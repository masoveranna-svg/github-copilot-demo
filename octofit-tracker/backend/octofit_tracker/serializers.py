from bson import ObjectId
from bson.errors import InvalidId
from rest_framework import serializers

from .models import Activity, Leaderboard, Team, User, Workout


class ObjectIdField(serializers.Field):
    def to_representation(self, value):
        return str(value)

    def to_internal_value(self, data):
        try:
            return ObjectId(str(data))
        except (InvalidId, TypeError):
            raise serializers.ValidationError('Invalid ObjectId.')


def user_reference(**kwargs):
    return serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), pk_field=ObjectIdField(), **kwargs
    )


def ensure_unique(serializer, model, field, value):
    # djongo cannot translate the .exists() query used by DRF's UniqueValidator
    queryset = model.objects.filter(**{field: value})
    if serializer.instance is not None:
        queryset = queryset.exclude(pk=serializer.instance.pk)
    if queryset.count():
        raise serializers.ValidationError(f'A {model.__name__.lower()} with this {field} already exists.')
    return value


class UserSerializer(serializers.ModelSerializer):
    _id = ObjectIdField(read_only=True)

    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'validators': []},
        }

    def validate_email(self, value):
        return ensure_unique(self, User, 'email', value)


class TeamSerializer(serializers.ModelSerializer):
    _id = ObjectIdField(read_only=True)
    members = user_reference(many=True, required=False)

    class Meta:
        model = Team
        fields = '__all__'
        extra_kwargs = {'name': {'validators': []}}

    def validate_name(self, value):
        return ensure_unique(self, Team, 'name', value)

    # members is an ArrayReferenceField, which must be set through its manager
    def create(self, validated_data):
        members = validated_data.pop('members', [])
        team = Team.objects.create(**validated_data)
        if members:
            team.members.set(members, clear=True)
        return team

    def update(self, instance, validated_data):
        members = validated_data.pop('members', None)
        instance = super().update(instance, validated_data)
        if members is not None:
            instance.members.set(members, clear=True)
        return instance


class ActivitySerializer(serializers.ModelSerializer):
    _id = ObjectIdField(read_only=True)
    user = user_reference()

    class Meta:
        model = Activity
        fields = '__all__'


class LeaderboardSerializer(serializers.ModelSerializer):
    _id = ObjectIdField(read_only=True)
    user = user_reference()
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Leaderboard
        fields = '__all__'


class WorkoutSerializer(serializers.ModelSerializer):
    _id = ObjectIdField(read_only=True)

    class Meta:
        model = Workout
        fields = '__all__'
