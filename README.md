# Shop Project - Tires and Disks E-Commerce Site

A Django-based e-commerce platform for selling car tires and disks.

## Features

- 👤 User registration and authentication
- 🛞 Tire catalog with detailed specifications
- 🎡 Disk catalog with technical parameters
- 📦 Shopping cart and order management
- 🖼️ Product image uploads
- 🔍 SEO-friendly URLs with slugs
- 📊 Admin panel for product management

## Tech Stack

- **Backend:** Django 5.0+
- **Database:** SQLite (development), PostgreSQL (production)
- **Python:** 3.9+

## Installation

### 1. Clone the repository
```bash
git clone https://github.com/1murs/web_site_120.git
cd web_site_120
```

### 2. Create virtual environment
```bash
python -m venv venv
```

### 3. Activate virtual environment

**On Windows:**
```bash
venv\Scripts\activate
```

**On macOS/Linux:**
```bash
source venv/bin/activate
```

### 4. Install dependencies
```bash
pip install -r requirements.txt
```

### 5. Run migrations
```bash
python manage.py migrate
```

### 6. Create superuser (admin account)
```bash
python manage.py createsuperuser
```

### 7. Start development server
```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` in your browser.

## Project Structure

```
web_site_120/
├── web_site_120/          # Main project settings
│   ├── settings.py       # Django settings
│   ├── urls.py           # URL routing
│   └── wsgi.py
├── users/                 # User management app
│   ├── models.py         # User model
│   └── ...
├── categories/            # Product categories app
│   ├── models.py         # Category model
│   └── ...
├── tires/                 # Tires app
│   ├── models.py         # Tire model
│   └── ...
├── disks/                 # Disks app
│   ├── models.py         # Disk model
│   └── ...
├── orders/                # Orders app
│   ├── models.py         # Order and OrderItem models
│   └── ...
├── media/                 # User uploaded files (tires/disks images)
├── db.sqlite3            # SQLite database
├── manage.py             # Django management script
└── requirements.txt      # Python dependencies
```

## Database Models

### User
- Registration and authentication
- Shipping address and contact information

### Category
- Product categories (Tires, Disks, etc.)
- SEO-friendly slugs

### Tire
- Brand, model, specifications (width, profile, diameter)
- Tire type, season, load index, speed index
- Price, stock quantity, image
- Auto-generated slug for URLs

### Disk
- Brand, model, specifications (diameter, width, PCD, DIA)
- Price, stock quantity, image
- Auto-generated slug for URLs

### Order
- Links to user and products
- Order status tracking (new, paid, shipped, delivered, cancelled)
- Total price calculation
- Timestamps for creation and updates

### OrderItem
- Individual items within an order
- Quantity and price (stored at time of order)
- Links to Tire or Disk products

## Admin Panel

Access Django admin panel at `http://127.0.0.1:8000/admin/`

Create a superuser first:
```bash
python manage.py createsuperuser
```

## Usage

### Add a new tire
1. Go to admin panel
2. Click "Tires" → "Add Tire"
3. Fill in all fields
4. Slug will be auto-generated
5. Upload an image
6. Save

### Add a new disk
Similar process as above in "Disks" section

## API Examples

```python
# Get all tires
from tires.models import Tire
all_tires = Tire.objects.all()

# Filter summer tires
summer_tires = Tire.objects.filter(season='summer')

# Get tires by brand
michelin_tires = Tire.objects.filter(brand='Michelin')

# Get tire by slug
tire = Tire.objects.get(slug='achilles-122-18560-r14')

# Get all disks
from disks.models import Disk
all_disks = Disk.objects.all()
```

## Contributing

Feel free to fork this project and submit pull requests!

## License

This project is open source and available under the MIT License.

## Author

Created as a learning project for Django e-commerce development.

## Support

For issues and questions, please create an issue on GitHub.
