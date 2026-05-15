import os

files = {
"app/templates/base.html": """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>Placement Cell</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet"/>
  <style>
    body { background: #f8f9fa; }
    .navbar { background: #1a1a2e; }
    .navbar-brand, .nav-link { color: #fff !important; }
  </style>
</head>
<body>
<nav class="navbar navbar-expand-lg">
  <div class="container">
    <a class="navbar-brand fw-bold" href="/">Placement Cell</a>
    <div class="ms-auto">
      {% if current_user.is_authenticated %}
        <span class="text-white me-3">Hello, {{ current_user.name }}</span>
        <a href="{{ url_for('auth.logout') }}" class="btn btn-outline-light btn-sm">Logout</a>
      {% else %}
        <a href="{{ url_for('auth.login') }}" class="btn btn-outline-light btn-sm me-2">Login</a>
        <a href="{{ url_for('auth.register') }}" class="btn btn-light btn-sm">Register</a>
      {% endif %}
    </div>
  </div>
</nav>
<div class="container mt-4">
  {% with messages = get_flashed_messages(with_categories=true) %}
    {% for category, message in messages %}
      <div class="alert alert-{{ category }} alert-dismissible fade show">
        {{ message }}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
      </div>
    {% endfor %}
  {% endwith %}
  {% block content %}{% endblock %}
</div>
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>""",

"app/templates/auth/login.html": """{% extends 'base.html' %}
{% block content %}
<div class="row justify-content-center mt-5">
  <div class="col-md-5">
    <div class="card shadow-sm">
      <div class="card-body p-4">
        <h3 class="mb-4 text-center fw-bold">Login</h3>
        <form method="POST">
          {{ form.hidden_tag() }}
          <div class="mb-3">
            {{ form.email.label(class="form-label") }}
            {{ form.email(class="form-control") }}
          </div>
          <div class="mb-3">
            {{ form.password.label(class="form-label") }}
            {{ form.password(class="form-control") }}
          </div>
          {{ form.submit(class="btn btn-primary w-100") }}
        </form>
        <hr/>
        <p class="text-center mb-0">No account?
          <a href="{{ url_for('auth.register') }}">Register here</a>
        </p>
      </div>
    </div>
  </div>
</div>
{% endblock %}""",

"app/templates/auth/register.html": """{% extends 'base.html' %}
{% block content %}
<div class="row justify-content-center mt-5">
  <div class="col-md-5">
    <div class="card shadow-sm">
      <div class="card-body p-4">
        <h3 class="mb-4 text-center fw-bold">Create Account</h3>
        <form method="POST">
          {{ form.hidden_tag() }}
          <div class="mb-3">
            {{ form.name.label(class="form-label") }}
            {{ form.name(class="form-control") }}
            {% for error in form.name.errors %}
              <small class="text-danger">{{ error }}</small>
            {% endfor %}
          </div>
          <div class="mb-3">
            {{ form.email.label(class="form-label") }}
            {{ form.email(class="form-control") }}
            {% for error in form.email.errors %}
              <small class="text-danger">{{ error }}</small>
            {% endfor %}
          </div>
          <div class="mb-3">
            {{ form.role.label(class="form-label") }}
            {{ form.role(class="form-select") }}
          </div>
          <div class="mb-3">
            {{ form.password.label(class="form-label") }}
            {{ form.password(class="form-control") }}
          </div>
          <div class="mb-3">
            {{ form.confirm.label(class="form-label") }}
            {{ form.confirm(class="form-control") }}
            {% for error in form.confirm.errors %}
              <small class="text-danger">{{ error }}</small>
            {% endfor %}
          </div>
          {{ form.submit(class="btn btn-success w-100") }}
        </form>
        <hr/>
        <p class="text-center mb-0">Already registered?
          <a href="{{ url_for('auth.login') }}">Login here</a>
        </p>
      </div>
    </div>
  </div>
</div>
{% endblock %}"""
}

for filepath, content in files.items():
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Created: {filepath}")

print("\nAll template files created successfully!")