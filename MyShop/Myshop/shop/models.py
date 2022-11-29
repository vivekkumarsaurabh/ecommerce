from django.db import models

class Product(models.Model):
    product_id = models.AutoField
    product_name = models.CharField(max_length=100)
    categories = models.CharField(max_length=50, default="")
    subcategories = models.CharField(max_length=50,default="")
    price = models.IntegerField(default=0)
    desc = models.CharField(max_length=300)
    pub_date = models.DateField()
    image = models.ImageField(upload_to="shop/images", default="")

    def __str__(self):
        return self.product_name




class Contact(models.Model):
    contact_id = models.AutoField(primary_key="True")
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100, default="")
    address = models.CharField(max_length=200,default="")
    mobile = models.CharField(max_length=20, default="")
    desc = models.CharField(max_length=500, default="")



    def __str__(self):
        return self.name


class Orders(models.Model):
    order_id = models.AutoField(primary_key=True)
    item_Json = models.CharField(max_length=8000)
    amount = models.IntegerField(default=0)
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100, default="")
    address = models.CharField(max_length=200,default="")
    address_2 = models.CharField(max_length=200,default="")
    city = models.CharField(max_length=200,default="")
    state = models.CharField(max_length=200,default="")
    zip_code = models.CharField(max_length=200,default="")
    mobile = models.CharField(max_length=20, default="")



    def __str__(self):
        return self.name


class OrderUpdate(models.Model):
    update_id = models.AutoField(primary_key=True)
    order_id = models.IntegerField(default="")
    update_desc = models.CharField(max_length=5000)
    timestamp = models.DateField(auto_now_add=True)


    def __str__(self):
        return self.update_desc[0:8] + "...."
