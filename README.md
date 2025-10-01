# 🍳 Django Recepten Project

Dit is een **Django project** voor recepten.  
De recepten betreffen uitsluitend **koken en braden**.  

⚠️ Let op: dit project is momenteel een **template** en moet nog verder worden opgezet. Het bevat enkel de Django-code als basis.

---

## 📂 Projectstatus
- [ ] Python **virtual environment (venv)** moet worden ingericht  
- [ ] `settings.py` moet nog worden opgezet  
- [ ] Geen MySQL-database inbegrepen (standaard SQLite kan worden gebruikt)  
- [ ] Geen Apache-configuratiebestand aanwezig  

---
## 🗂 Voorbeeld projectstructuur

├── README.md
├── VERSION
├── apps
│   ├── __init__.py
│   ├── recepten
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── forms.py
│   │   ├── models
│   │   │   ├── __init__.py
│   │   │   ├── categorie.py
│   │   │   ├── gerechttype.py
│   │   │   ├── ingredient.py
│   │   │   └── recept.py
│   │   ├── templates
│   │   │   └── recepten
│   │   │       ├── categorie_confirm_delete.html
│   │   │       ├── categorie_invoer.html
│   │   │       ├── categorie_lijst.html
│   │   │       ├── gerecht_type_confirm_delete.html
│   │   │       ├── gerecht_type_invoer.html
│   │   │       ├── gerecht_type_lijst.html
│   │   │       ├── ingredient_conform_delete.html
│   │   │       ├── ingredient_invoer.html
│   │   │       ├── ingredient_lijst.html
│   │   │       ├── maintenance.html
│   │   │       ├── recept_confirm_delete.html
│   │   │       ├── recept_detail.html
│   │   │       ├── recept_invoer.html
│   │   │       ├── recept_lijst.html
│   │   │       ├── recept_pdf.html
│   │   │       ├── recept_zoek.html
│   │   │       └── welkom.html
│   │   ├── templatetags
│   │   │   ├── __init__.py
│   │   │   └── form_tags.py
│   │   ├── tests.py
│   │   ├── urls.py
│   │   ├── utils.py
│   │   └── views
│   │       ├── __init__.py
│   │       ├── categorie.py
│   │       ├── gerecht_type.py
│   │       ├── ingredient.py
│   │       ├── recept_pdf.py
│   │       ├── recept_zoek.py
│   │       ├── recepten.py
│   │       └── welkom.py
│   └── users
│       ├── __init__.py
│       ├── admin.py
│       ├── apps.py
│       ├── decorators.py
│       ├── models.py
│       ├── templates
│       │   └── users
│       │       ├── create_user.html
│       │       ├── login.html
│       │       ├── password_change.html
│       │       └── password_change_done.html
│       ├── templatetags
│       │   ├── __init__.py
│       │   └── user_tags.py
│       ├── tests.py
│       ├── urls.py
│       └── views.py
├── config
│   ├── __init__.py
│   ├── asgi.py
│   ├── context_processors.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── manage.py
├── requirements.txt
├── static
│   ├── css
│   │   ├── base.css
│   │   ├── dropdown.css
│   │   ├── layout.css
│   │   ├── menu-collapsed.css
│   │   ├── navbar.css
│   │   ├── pdf.css
│   │   ├── recept.css
│   │   ├── responsive.css
│   │   ├── user-menu.css
│   │   └── welkom.css
│   └── images
│       ├── placeholder.png
│       └── welkom.jpeg
└── templates
    ├── base.html
    └── partials
        ├── menu.html
        └── stylesheets.html

