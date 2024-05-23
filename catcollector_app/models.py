from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

MEALS = (
    ('B', 'Breakfast'),
    ('L', 'Lunch'),
    ('D', 'Dinner'),
)

class Toy(models.Model):
    name = models.CharField(max_length=50)
    color = models.CharField(max_length=20)

    def __str__(self):
        return self.name
    
    #absolute path that this will live on
    def get_absolute_url(self):
        return reverse('toys_detail', kwargs={'pk': self.id})

# Create your models here.
class Cat(models.Model):
    name = models.CharField(max_length=100)
    breed = models.CharField(max_length=100)
    description = models.TextField(max_length=250)
    age = models.IntegerField()
    toys = models.ManyToManyField(Toy)
    #cat.toys --> toys owned by the cat
    #toys.cat_set --> cats associated with a single toy
    user = models.ForeignKey(User, on_delete=models.CASCADE)


    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('detail', kwargs={'cat_id': self.id})

class Feeding(models.Model):
    date = models.DateField('feeding date')
    meal = models.CharField(
        max_length=1,
        choices=MEALS,
        default=MEALS[0][0]
    )
    # on delete, they will remove all feeding instances related to the deleted cat
    cat = models.ForeignKey(Cat, on_delete=models.CASCADE)
    # syntax for accessing all the feedings thorugh the parent: parent.child_set.all() --> Cat.feeding)set.all()
    # syntax for accessing the parent through the child: Child.field.all() --> Feeding.cat.all()

    def __str__(self):
        return f"{self.get_meal_display()} on {self.date}"
        #return "Dinner on 2024-05-04"

    # change the default sort
    class Meta:
        ordering = ['-date'] #descending order

class Photo(models.Model):
    url = models.CharField(max_length=200)
    cat = models.ForeignKey(Cat, on_delete=models.CASCADE)

    def __str__(self):
        return f"Photo for cat_id: {self.cat_id} @ {self.url}"

    #Photo for cat_id: 5 @https://