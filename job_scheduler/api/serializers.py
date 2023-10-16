import datetime

from rest_framework import serializers

from scheduler.models import Month, Day, Worker


class WorkerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Worker
        fields = ('id', 'name')

    def validate_name(self, value):
        if not self.instance:
            return ' '.join(word.capitalize() for word in value.split())
        return value


class DaySerializer(serializers.ModelSerializer):
    workers = WorkerSerializer(many=True)

    class Meta:
        model = Day
        fields = ('id', 'day_number', 'workers_required', 'workers')


class MonthSerializer(serializers.ModelSerializer):
    days = DaySerializer(many=True, read_only=True, source='day_set')

    class Meta:
        model = Month
        fields = ('id', 'year', 'month_number', 'days')

    def validate(self, data):
        year = data.get('year')
        month = data.get('month_number')
        now = datetime.datetime.now()

        if year < now.year or year == now.year and now.month > month:
            raise serializers.ValidationError('There is no point in making a schedule for the past time')

        return data
