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

```text
recepten_project/        <-- hoofdproject
│
├── manage.py            <-- Django management script
├── requirements.txt     <-- (optioneel) dependencies
│
├── recepten_project/    <-- hoofdconfiguratie van Django
│   ├── __init__.py
│   ├── settings.py      <-- moet nog worden opgezet
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
│
└── recepten/            <-- app voor recepten
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    ├── models.py        <-- modellen voor recepten
    ├── tests.py
    └── views.py         <-- views voor recepten


