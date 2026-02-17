from django import forms


from apps.dashboard.models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["title", "content"]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'w-full rounded border border-gray-300 py-2 px-3 focus:ring-2 focus:ring-blue-300', "placeholder":"Add title"}),
            'content': forms.Textarea(attrs={'class': 'w-full rounded border border-gray-300 py-2 px-3 focus:ring-2 focus:ring-blue-300', "placeholder":"Write something..."}),
        }