from django.db import models
from django.contrib.auth.models import User



class Category(models.Model):
    """
    #### Class :

        Definition of `Category` model.

    #### Attributes:

        - `title`   : str
        - `slug`    : str
        
    
    """
    title = models.CharField( max_length=255,db_index=True)
    slug = models.SlugField(max_length=255)

    def __str__(self) -> str:
        return self.title

class MenuItem(models.Model):
    """
    #### Class :

        Definition of `MenuItem` model.

    #### Attributes:
        - `title`    : str
        - `price`    : float
        - `stock`    : int
        - `featured` : bool
        - `category` : `Category`
    
    """
    title = models.CharField( max_length=255,db_index=True)
    price = models.DecimalField(max_digits=6, decimal_places=2,db_index=True)
    stock = models.SmallIntegerField(default=0.0)
    featured = models.BooleanField(db_index=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    
    def __str__(self) -> str:
        return self.title

class Cart(models.Model):
    """
    #### Class :

        Definition of `Cart` model.

    #### Attributes:
        - `user`    : `User`
        - `menuitem`    : `MenuItem`
        - `quantity`    : int
        - `unit_price` : float
        - `price` : float
    
    """
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    menuitem = models.ForeignKey(MenuItem,on_delete=models.CASCADE)
    quantity = models.SmallIntegerField()
    unit_price = models.DecimalField(max_digits=6,decimal_places=2)
    price = models.DecimalField(max_digits=6,decimal_places=2)

    class Meta:
        unique_together = ('menuitem','user') # There can be only one menu item entry for a specific user

class Order(models.Model):
    """
    #### Class :

        Definition of `Order` model.

    #### Attributes:
        - `user`    : `User`
        - `delivery_crew`    : `User`
        - `status`    : bool
        - `total` : float
        - `data` : `Date` 
    
    """
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    delivery_crew = models.ForeignKey(User,on_delete=models.SET_NULL,related_name="delivery_crew",null=True)
    status = models.BooleanField(db_index=True,default=0)
    total = models.DecimalField(max_digits=6,decimal_places=2)
    date = models.DateField(db_index=True,auto_now_add=True,blank=True, null=True)
    
class OrderItem(models.Model):
    """
    #### Class :

        Definition of `OrderItem` model.

    #### Attributes:
        - `order`    : `Order`
        - `menuitem`    : `MenuItem`
        - `quantity`    : int
        - `unit_price` : float
    
    """
    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    menuitem = models.ForeignKey(MenuItem,on_delete=models.CASCADE)
    quantity = models.SmallIntegerField()
    unit_price = models.DecimalField(max_digits=6,decimal_places=2)

    class Meta:
        unique_together = ('order','menuitem') # One order can have only one entry for a specific menu item


    def __str__(self) -> str:
        return  f"Order : {self.quantity}  {self.menuitem.title}"