from django.db import models

from core.models import UUIDModel, TimeStampedModel, StatusModel


class Role(UUIDModel, TimeStampedModel, StatusModel):
    """
    Master table for ERP roles.
    Example: Admin, Purchase, Accounts, QC, Store, Sales
    """

    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        db_table = "master_roles"
        verbose_name = "Role"
        verbose_name_plural = "Roles"

    def __str__(self):
        return self.name


class Department(UUIDModel, TimeStampedModel, StatusModel):
    """
    Organizational department master.
    Example: Purchase, Accounts, Production, Sales
    """

    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        db_table = "master_departments"
        verbose_name = "Department"
        verbose_name_plural = "Departments"

    def __str__(self):
        return self.name


class Warehouse(UUIDModel, TimeStampedModel, StatusModel):
    """
    Warehouse / stock location master.
    """

    name = models.CharField(max_length=150, unique=True)
    code = models.CharField(max_length=50, unique=True)
    address = models.TextField(blank=True)

    class Meta:
        db_table = "master_warehouses"
        verbose_name = "Warehouse"
        verbose_name_plural = "Warehouses"

    def __str__(self):
        return self.name


class UnitOfMeasure(UUIDModel, TimeStampedModel, StatusModel):
    """
    Unit of Measure (UOM) master.
    Example: KG, NOS, MTR, LTR
    """

    name = models.CharField(max_length=50, unique=True)
    code = models.CharField(max_length=20, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        db_table = "master_uoms"
        verbose_name = "Unit of Measure"
        verbose_name_plural = "Units of Measure"

    def __str__(self):
        return self.code


class Tax(UUIDModel, TimeStampedModel, StatusModel):
    """
    Tax master (GST / VAT / others).
    """

    name = models.CharField(max_length=100)
    code = models.CharField(max_length=50, unique=True)
    rate = models.DecimalField(max_digits=5, decimal_places=2)
    description = models.TextField(blank=True)

    class Meta:
        db_table = "master_taxes"
        verbose_name = "Tax"
        verbose_name_plural = "Taxes"

    def __str__(self):
        return f"{self.code} ({self.rate}%)"


class Bank(UUIDModel, TimeStampedModel, StatusModel):
    """
    Bank master.
    """

    name = models.CharField(max_length=150)
    branch = models.CharField(max_length=150, blank=True)
    ifsc_code = models.CharField(max_length=20, unique=True)
    swift_code = models.CharField(max_length=20, blank=True)

    class Meta:
        db_table = "master_banks"
        verbose_name = "Bank"
        verbose_name_plural = "Banks"

    def __str__(self):
        return f"{self.name} - {self.ifsc_code}"


class Vendor(UUIDModel, TimeStampedModel, StatusModel):
    """
    Vendor master.
    Represents suppliers from whom goods/services are procured.
    """

    name = models.CharField(max_length=255, unique=True)

    code = models.CharField(max_length=50, unique=True, help_text="Unique vendor code")

    contact_person = models.CharField(max_length=255, blank=True)

    phone = models.CharField(max_length=50, blank=True)

    email = models.EmailField(blank=True)

    address = models.TextField(blank=True)

    gst_number = models.CharField(
        max_length=50, blank=True, help_text="GST / Tax identification number"
    )

    country = models.CharField(max_length=100, blank=True)

    class Meta:
        db_table = "master_vendors"
        verbose_name = "Vendor"
        verbose_name_plural = "Vendors"

    def __str__(self):
        return f"{self.code} - {self.name}"


class Customer(UUIDModel, TimeStampedModel, StatusModel):
    """
    Customer master.
    Represents customers to whom goods/services are sold.
    """

    name = models.CharField(max_length=255, unique=True)

    code = models.CharField(
        max_length=50, unique=True, help_text="Unique customer code"
    )

    contact_person = models.CharField(max_length=255, blank=True)

    phone = models.CharField(max_length=50, blank=True)

    email = models.EmailField(blank=True)

    address = models.TextField(blank=True)

    gst_number = models.CharField(
        max_length=50, blank=True, help_text="GST / Tax identification number"
    )

    country = models.CharField(max_length=100, blank=True)

    class Meta:
        db_table = "master_customers"
        verbose_name = "Customer"
        verbose_name_plural = "Customers"

    def __str__(self):
        return f"{self.code} - {self.name}"
