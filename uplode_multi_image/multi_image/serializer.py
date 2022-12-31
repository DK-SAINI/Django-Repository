from rest_framework import serializers

from multi_image.models import Student, StudentImage


class StudentImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentImage
        fields = "__all__"


class StudentSerializer(serializers.ModelSerializer):
    multi_image = StudentImageSerializer(many=True, read_only=True)

    class Meta:
        model = Student
        fields = ["name", "remarks", "multi_image"]

    def create(self, validated_data):
        images_data = self.context.get('request').getlist('multi_image')
        student = Student.objects.create(**validated_data)
        for img in images_data:
            StudentImage.objects.create(student=student, image=img)
        return student
