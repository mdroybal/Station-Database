from django.contrib import admin
from .models import TireInvSize,TireInvBrand,TireInventory,TireSale,Customer,AccountReceivable,Charge,Payment


@admin.register(TireInvSize)
class TireInvSizeAdmin(admin.ModelAdmin):
	list_display = ('id','size')
	fields = ['size']
	ordering = ['size']

	def get_readonly_fields(self,request,obj=None):
	    if obj:
	        return self.readonly_fields + ('size')
	    return self.readonly_fields

	# def has_delete_permission(self, request, obj=None):
	# 	return False

	# def get_actions(self, request):
	# 	actions = super(TireInvSize, self).get_actions(request)
	# 	if 'delete_selected' in actions:
	# 		del actions['delete_selected']
	# 	return actions


@admin.register(TireInvBrand)
class TireInvBrandAdmin(admin.ModelAdmin):
	list_display = ('id','brand')
	fields = ['brand']
	ordering = ['brand']

	def get_readonly_fields(self,request,obj=None):
	    if obj:
	        return self.readonly_fields + ('brand')
	    return self.readonly_fields

	# def has_delete_permission(self, request, obj=None):
	# 	return False

	# def get_actions(self, request):
	# 	actions = super(TireInvBrand, self).get_actions(request)
	# 	if 'delete_selected' in actions:
	# 		del actions['delete_selected']
	# 	return actions


@admin.register(TireInventory)
class TireInventoryAdmin(admin.ModelAdmin):
	list_display = ('__unicode__','quantity','supplier_code','unit_cost','total_unit_cost','retail_price')
	fields = ['size','brand','supplier_code',('quantity','unit_cost'),'retail_price']
	list_filter = ('size','brand')
	ordering = ['size','brand']

	def get_readonly_fields(self,request,obj=None):
		if obj:
		    return self.readonly_fields + ('size','brand','supplier_code')
		return self.readonly_fields

	def has_delete_permission(self, request, obj=None):
		return False

	def get_actions(self, request):
		actions = super(TireInventoryAdmin, self).get_actions(request)
		if 'delete_selected' in actions:
			del actions['delete_selected']
		return actions


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
	list_display = ('__unicode__','phone_number','address')
	fields = ['first_name','middle_name','last_name','phone_number','address']
	list_filter = ('last_name','middle_name')
	ordering = ['last_name','first_name']

	def get_readonly_fields(self,request,obj=None):
		if obj:
		    return self.readonly_fields + ('first_name','middle_name','last_name')
		return self.readonly_fields

	def has_delete_permission(self, request, obj=None):
		return False

	def get_actions(self, request):
		actions = super(CustomerAdmin, self).get_actions(request)
		if 'delete_selected' in actions:
			del actions['delete_selected']
		return actions


@admin.register(TireSale)
class TireSaleAdmin(admin.ModelAdmin):
	list_display = ('customer','date_of_purchase','tires','total_price','rotation_mileage','rotation_performed','notes')
	fields = ['customer','tires','quantity','date_of_purchase','total_price','mileage','amount_paid','notes','rotation_performed']
	list_filter = ('customer','date_of_purchase')
	ordering = ['customer','date_of_purchase']

	def get_readonly_fields(self,request,obj=None):
	    if obj:
	        return self.readonly_fields + ('customer', 'mileage','date_of_purchase','tires','total_price','quantity','amount_paid')
	    return self.readonly_fields

	def has_delete_permission(self, request, obj=None):
		return False

	def get_actions(self, request):
		actions = super(TireSaleAdmin, self).get_actions(request)
		if 'delete_selected' in actions:
			del actions['delete_selected']
		return actions


@admin.register(AccountReceivable)
class AccountReceivableAdmin(admin.ModelAdmin):
	list_display = ('customer','due_date','current_balance','past_due','notes')
	fields = ['customer','due_date','current_balance','notes']
	list_filter = ('customer','due_date')
	ordering = ['customer','due_date']

	def get_readonly_fields(self,request,obj=None):
		if obj:
		    return self.readonly_fields + ('customer','current_balance')
		return self.readonly_fields

	def has_delete_permission(self, request, obj=None):
		return False

	def get_actions(self, request):
		actions = super(AccountReceivableAdmin, self).get_actions(request)
		if 'delete_selected' in actions:
			del actions['delete_selected']
		return actions
    

@admin.register(Charge)
class ChargeAdmin(admin.ModelAdmin):
	list_display = ('invoice_number','customer','date','due_date','charge','note')
	fields = ['invoice_number','customer','date','due_date','charge','note']
	list_filter = ('customer','date')
	ordering = ['date','customer']

	def get_readonly_fields(self,request,obj=None):
		if obj:
		    return self.readonly_fields + ('customer','date','charge','note','invoice_number','due_date')
		return self.readonly_fields

	def has_delete_permission(self, request, obj=None):
		return False

	def get_actions(self, request):
		actions = super(ChargeAdmin, self).get_actions(request)
		if 'delete_selected' in actions:
			del actions['delete_selected']
		return actions


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
	list_display = ('invoice_number','customer','payment_date','payment','note')
	fields = ['invoice_number','customer','payment_date','payment','note']
	list_filter = ('customer','payment_date')
	ordering = ['payment_date','customer']

	def get_readonly_fields(self,request,obj=None):
		if obj:
		    return self.readonly_fields + ('customer','payment_date','payment','note','invoice_number')
		return self.readonly_fields

	def has_delete_permission(self, request, obj=None):
		return False

	def get_actions(self, request):
		actions = super(PaymentAdmin, self).get_actions(request)
		if 'delete_selected' in actions:
			del actions['delete_selected']
		return actions


