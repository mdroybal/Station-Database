from django.db import models
from django.utils.timezone import datetime,timedelta
from django.utils.encoding import python_2_unicode_compatible


class Customer(models.Model):
	first_name = models.CharField(max_length=64)
	last_name = models.CharField(max_length=64)
	middle_name = models.CharField(max_length=48,blank=True)
	phone_number = models.CharField(max_length=48,blank=True)
	address = models.CharField(max_length=256,blank=True)

	class Meta:
		unique_together = ('first_name','last_name','middle_name')
		ordering = ['last_name','first_name']

	def __unicode__(self):
		return '%s %s %s' % (self.first_name,self.middle_name,self.last_name) 

class TireInvSize(models.Model):
	size = models.CharField(max_length=64,unique=True)

	class Meta:
		ordering = ['size']

	def __unicode__(self):
		return '%s' % (self.size)	

class TireInvBrand(models.Model):
	brand = models.CharField(max_length=64,unique=True)

	class Meta:
	    ordering = ['brand']

	def __unicode__(self):
		return '%s' % (self.brand)	


class TireInventory(models.Model):
	supplier_list = ['ATD','FT','RR','Other']
	suppliers = ((supplier_list[0],'ATD'),(supplier_list[1],'FT'),(supplier_list[2],'RR'),(supplier_list[3],'Other'))
	size = models.ForeignKey(TireInvSize)
	brand = models.ForeignKey(TireInvBrand)
	quantity = models.IntegerField()
	unit_cost = models.DecimalField(max_digits=8,decimal_places=2)
	retail_price = models.DecimalField(max_digits=6,decimal_places=2,null=True,blank=True)
	supplier_code = models.CharField(choices=suppliers,max_length=16)

	@property
	def total_unit_cost(self):
		return (self.unit_cost * self.quantity)
	class Meta:
		unique_together = ('size','brand','supplier_code')
		ordering = ['size','brand']

	def __unicode__(self):
	    return '%s %s' % (self.size,self.brand)


@python_2_unicode_compatible
class TireSale(models.Model):
	customer = models.ForeignKey(Customer)
	tires = models.ForeignKey(TireInventory)
	date_of_purchase = models.DateField(default=datetime.today())
	total_price = models.DecimalField(max_digits=6,decimal_places=2)
	amount_paid = models.DecimalField(max_digits=6,decimal_places=2,null=True,blank=True)
	quantity = models.IntegerField()
	mileage = models.IntegerField(default=0,null=True,blank=True)
	rotation_performed = models.BooleanField(default=False)
	notes = models.CharField(max_length=256,blank=True)
    
	@property
	def rotation_mileage(self):
		if self.quantity >= 4:
		    return (int(self.mileage) + 10000)
		else:
			return ("")

	def save(self,*args,**kwargs):		
		tire_obj = TireInventory.objects.get(id=self.tires.id)
		tire_obj.quantity -= self.quantity
		tire_obj.save()
		super(TireSale,self).save(*args,**kwargs)

	class Meta:
	    ordering = ['customer','date_of_purchase']
	
	def __str__(self):
		return "Tire Sale #{}".format(self.id)


@python_2_unicode_compatible
class AccountReceivable(models.Model):
	due_date = models.DateField(default=datetime.today()+timedelta(days=30))
	customer = models.ForeignKey(Customer,unique=True)
	notes = models.CharField(max_length=256,blank=True)
	current_balance = models.DecimalField(max_digits=7,decimal_places=2)
	
	@property
	def past_due(self):
		if self.due_date < datetime.now().date():
		    return "{} days".format(abs(((self.due_date - datetime.now().date()).days)))
		else:
			return ("")
	class Meta:
	    ordering = ['customer','due_date']

	def __str__(self):
		return "{}".format(self.customer)


@python_2_unicode_compatible
class Charge(models.Model):
	invoice_number = models.CharField(primary_key=True,max_length=32)
	date = models.DateField(default=datetime.today()-timedelta(days=1))
	due_date = models.DateField(default=datetime.today()+timedelta(days=30))
	customer = models.ForeignKey(AccountReceivable)
	charge = models.DecimalField(max_digits=7,decimal_places=2)
	note = models.CharField(max_length=128,blank=True)    

	def save(self,*args,**kwargs):
		ar_obj = AccountReceivable.objects.get(id=self.customer.id)
		try:
			charge_obj = Charge.objects.filter(customer=self.customer.id).order_by('due_date')[0]
			ar_obj.due_date = charge_obj.due_date	

		except IndexError:
			print "Please add more charges!" 

		ar_obj.current_balance += self.charge
		ar_obj.save()
		super(Charge,self).save(*args,**kwargs)

	class Meta:
	    ordering = ['date','customer']

	def __str__(self):
		return "Charge #{}".format(self.invoice_number)


@python_2_unicode_compatible
class Payment(models.Model):
	invoice_number = models.CharField(primary_key=True,max_length=32)
	payment_date = models.DateField(default=datetime.today())
	customer = models.ForeignKey(AccountReceivable)
	payment = models.DecimalField(max_digits=7,decimal_places=2)
	note = models.CharField(max_length=128,blank=True)

	def save(self,*args,**kwargs):
		ar_obj = AccountReceivable.objects.get(id=self.customer.id)
		ar_obj.current_balance -= self.payment
		ar_obj.save()
		super(Payment,self).save(*args,**kwargs)

	class Meta:
	    ordering = ['payment_date','customer']

	def __str__(self):
		return "Payment #{}".format(self.invoice_number)