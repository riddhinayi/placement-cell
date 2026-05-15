import os

files = {

"app/templates/base.html": """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>{% block title %}Placement Cell{% endblock %}</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet"/>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.5/font/bootstrap-icons.css" rel="stylesheet"/>
  <style>
    body { background: #f0f2f5; font-family: 'Segoe UI', sans-serif; }

    /* Navbar */
    .navbar { background: linear-gradient(135deg, #1a1a2e, #16213e); box-shadow: 0 2px 10px rgba(0,0,0,0.3); }
    .navbar-brand { font-size: 1.3rem; font-weight: 700; color: #fff !important; letter-spacing: 0.5px; }
    .navbar-brand span { color: #4cc9f0; }
    .nav-link { color: rgba(255,255,255,0.85) !important; font-size: 0.9rem; }
    .nav-link:hover { color: #4cc9f0 !important; }
    .nav-user { color: #a8d8ea; font-size: 0.85rem; }

    /* Cards */
    .card { border: none; border-radius: 12px; box-shadow: 0 2px 12px rgba(0,0,0,0.08); }
    .card-header { background: #fff; border-bottom: 1px solid #f0f0f0;
                   border-radius: 12px 12px 0 0 !important; font-weight: 600; padding: 1rem 1.25rem; }

    /* Stat cards */
    .stat-card { border-radius: 12px; padding: 1.25rem; color: white; }
    .stat-card h3 { font-size: 2rem; font-weight: 700; margin: 0; }
    .stat-card p  { margin: 0; opacity: 0.9; font-size: 0.9rem; }

    /* Buttons */
    .btn { border-radius: 8px; font-size: 0.875rem; }
    .btn-primary   { background: #4361ee; border-color: #4361ee; }
    .btn-success   { background: #2dc653; border-color: #2dc653; }

    /* Tables */
    .table { margin: 0; }
    .table thead th { font-size: 0.8rem; text-transform: uppercase;
                      letter-spacing: 0.5px; padding: 0.85rem 1rem; }
    .table tbody td { padding: 0.85rem 1rem; vertical-align: middle; font-size: 0.9rem; }
    .table-hover tbody tr:hover { background: #f8f9ff; }

    /* Badges */
    .badge { border-radius: 6px; font-weight: 500; font-size: 0.75rem; padding: 4px 8px; }

    /* Sidebar role label */
    .role-badge { font-size: 0.7rem; padding: 2px 8px; border-radius: 20px;
                  background: rgba(255,255,255,0.15); color: #fff; margin-left: 6px; }

    /* Page header */
    .page-header { margin-bottom: 1.5rem; }
    .page-header h2 { font-weight: 700; color: #1a1a2e; font-size: 1.6rem; }
    .page-header p  { color: #6c757d; margin: 0; }

    /* Alert */
    .alert { border-radius: 10px; border: none; }

    /* Footer */
    .footer { margin-top: 3rem; padding: 1.5rem 0; text-align: center;
              color: #adb5bd; font-size: 0.85rem; border-top: 1px solid #e9ecef; }
  </style>
</head>
<body>

<!-- NAVBAR -->
<nav class="navbar navbar-expand-lg">
  <div class="container">
    <a class="navbar-brand" href="/">
      <i class="bi bi-mortarboard-fill me-2"></i>Placement<span>Cell</span>
    </a>

    <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navMenu">
      <span class="navbar-toggler-icon"></span>
    </button>

    <div class="collapse navbar-collapse" id="navMenu">
      <ul class="navbar-nav me-auto">
        {% if current_user.is_authenticated %}

          {% if current_user.role == 'admin' %}
            <li class="nav-item">
              <a class="nav-link" href="{{ url_for('admin.dashboard') }}">
                <i class="bi bi-speedometer2 me-1"></i>Dashboard
              </a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="{{ url_for('admin.students') }}">
                <i class="bi bi-people me-1"></i>Students
              </a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="{{ url_for('admin.companies') }}">
                <i class="bi bi-building me-1"></i>Companies
              </a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="{{ url_for('admin.drives') }}">
                <i class="bi bi-briefcase me-1"></i>Drives
              </a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="{{ url_for('admin.applications') }}">
                <i class="bi bi-file-earmark-text me-1"></i>Applications
              </a>
            </li>

          {% elif current_user.role == 'student' %}
            <li class="nav-item">
              <a class="nav-link" href="{{ url_for('student.dashboard') }}">
                <i class="bi bi-speedometer2 me-1"></i>Dashboard
              </a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="{{ url_for('student.drives') }}">
                <i class="bi bi-briefcase me-1"></i>Job Drives
              </a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="{{ url_for('student.my_applications') }}">
                <i class="bi bi-file-earmark-check me-1"></i>My Applications
              </a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="{{ url_for('student.profile') }}">
                <i class="bi bi-person-circle me-1"></i>My Profile
              </a>
            </li>

          {% elif current_user.role == 'company' %}
            <li class="nav-item">
              <a class="nav-link" href="{{ url_for('company.dashboard') }}">
                <i class="bi bi-speedometer2 me-1"></i>Dashboard
              </a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="{{ url_for('company.my_drives') }}">
                <i class="bi bi-briefcase me-1"></i>My Drives
              </a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="{{ url_for('company.new_drive') }}">
                <i class="bi bi-plus-circle me-1"></i>Post Drive
              </a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="{{ url_for('company.profile') }}">
                <i class="bi bi-building me-1"></i>Company Profile
              </a>
            </li>
          {% endif %}

        {% endif %}
      </ul>

      <!-- Right side -->
      <ul class="navbar-nav ms-auto align-items-center">
        {% if current_user.is_authenticated %}
          <li class="nav-item me-2">
            <span class="nav-user">
              <i class="bi bi-person-fill me-1"></i>{{ current_user.name }}
              <span class="role-badge">{{ current_user.role }}</span>
            </span>
          </li>
          <li class="nav-item">
            <a href="{{ url_for('auth.logout') }}"
               class="btn btn-sm btn-outline-light">
              <i class="bi bi-box-arrow-right me-1"></i>Logout
            </a>
          </li>
        {% else %}
          <li class="nav-item me-2">
            <a href="{{ url_for('auth.login') }}"
               class="btn btn-sm btn-outline-light">Login</a>
          </li>
          <li class="nav-item">
            <a href="{{ url_for('auth.register') }}"
               class="btn btn-sm btn-light text-dark">Register</a>
          </li>
        {% endif %}
      </ul>
    </div>
  </div>
</nav>

<!-- FLASH MESSAGES -->
<div class="container mt-3">
  {% with messages = get_flashed_messages(with_categories=true) %}
    {% for category, message in messages %}
      <div class="alert alert-{{ category }} alert-dismissible fade show" role="alert">
        <i class="bi bi-info-circle me-2"></i>{{ message }}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
      </div>
    {% endfor %}
  {% endwith %}
</div>

<!-- MAIN CONTENT -->
<div class="container mt-3 mb-5">
  {% block content %}{% endblock %}
</div>

<!-- FOOTER -->
<div class="footer">
  <div class="container">
    <i class="bi bi-mortarboard-fill me-1"></i>
    Placement Cell Management System &mdash; Built with Flask &amp; Python
  </div>
</div>

<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>""",

# ── POLISHED LOGIN ─────────────────────────────────────────────────────────────
"app/templates/auth/login.html": """{% extends 'base.html' %}
{% block title %}Login | Placement Cell{% endblock %}
{% block content %}
<div class="row justify-content-center mt-4">
  <div class="col-md-10">
    <div class="row shadow rounded-4 overflow-hidden bg-white">

      <!-- Left panel -->
      <div class="col-md-5 d-none d-md-flex flex-column justify-content-center align-items-center p-5"
           style="background: linear-gradient(135deg, #1a1a2e, #4361ee);">
        <i class="bi bi-mortarboard-fill text-white" style="font-size:4rem;"></i>
        <h3 class="text-white fw-bold mt-3">Placement Cell</h3>
        <p class="text-white-50 text-center mt-2">
          Your gateway to campus placements. Login to continue.
        </p>
        <hr class="w-75 border-white opacity-25"/>
        <p class="text-white-50 text-center small">
          Admin &bull; Student &bull; Company &mdash; All roles in one place
        </p>
      </div>

      <!-- Right panel / form -->
      <div class="col-md-7 p-5">
        <h4 class="fw-bold mb-1">Welcome back!</h4>
        <p class="text-muted mb-4">Sign in to your account</p>
        <form method="POST">
          {{ form.hidden_tag() }}
          <div class="mb-3">
            {{ form.email.label(class="form-label fw-semibold") }}
            <div class="input-group">
              <span class="input-group-text"><i class="bi bi-envelope"></i></span>
              {{ form.email(class="form-control", placeholder="you@email.com") }}
            </div>
          </div>
          <div class="mb-4">
            {{ form.password.label(class="form-label fw-semibold") }}
            <div class="input-group">
              <span class="input-group-text"><i class="bi bi-lock"></i></span>
              {{ form.password(class="form-control", placeholder="Password") }}
            </div>
          </div>
          {{ form.submit(class="btn btn-primary w-100 py-2") }}
        </form>
        <hr/>
        <p class="text-center text-muted mb-0">
          No account? <a href="{{ url_for('auth.register') }}">Register here</a>
        </p>
        <p class="text-center text-muted small mt-2">
          <strong>Admin login:</strong> admin@placement.com / admin123
        </p>
      </div>

    </div>
  </div>
</div>
{% endblock %}""",

# ── POLISHED REGISTER ──────────────────────────────────────────────────────────
"app/templates/auth/register.html": """{% extends 'base.html' %}
{% block title %}Register | Placement Cell{% endblock %}
{% block content %}
<div class="row justify-content-center mt-4">
  <div class="col-md-6">
    <div class="card p-4">
      <div class="text-center mb-4">
        <i class="bi bi-person-plus-fill text-primary" style="font-size:2.5rem;"></i>
        <h4 class="fw-bold mt-2">Create Account</h4>
        <p class="text-muted">Join the placement portal</p>
      </div>
      <form method="POST">
        {{ form.hidden_tag() }}
        <div class="mb-3">
          {{ form.name.label(class="form-label fw-semibold") }}
          <div class="input-group">
            <span class="input-group-text"><i class="bi bi-person"></i></span>
            {{ form.name(class="form-control", placeholder="Your full name") }}
          </div>
          {% for e in form.name.errors %}
            <small class="text-danger">{{ e }}</small>
          {% endfor %}
        </div>
        <div class="mb-3">
          {{ form.email.label(class="form-label fw-semibold") }}
          <div class="input-group">
            <span class="input-group-text"><i class="bi bi-envelope"></i></span>
            {{ form.email(class="form-control", placeholder="you@email.com") }}
          </div>
          {% for e in form.email.errors %}
            <small class="text-danger">{{ e }}</small>
          {% endfor %}
        </div>
        <div class="mb-3">
          {{ form.role.label(class="form-label fw-semibold") }}
          {{ form.role(class="form-select") }}
        </div>
        <div class="mb-3">
          {{ form.password.label(class="form-label fw-semibold") }}
          <div class="input-group">
            <span class="input-group-text"><i class="bi bi-lock"></i></span>
            {{ form.password(class="form-control", placeholder="Min 6 characters") }}
          </div>
        </div>
        <div class="mb-4">
          {{ form.confirm.label(class="form-label fw-semibold") }}
          <div class="input-group">
            <span class="input-group-text"><i class="bi bi-lock-fill"></i></span>
            {{ form.confirm(class="form-control", placeholder="Repeat password") }}
          </div>
          {% for e in form.confirm.errors %}
            <small class="text-danger">{{ e }}</small>
          {% endfor %}
        </div>
        {{ form.submit(class="btn btn-success w-100 py-2") }}
      </form>
      <hr/>
      <p class="text-center mb-0 text-muted">
        Already registered? <a href="{{ url_for('auth.login') }}">Login here</a>
      </p>
    </div>
  </div>
</div>
{% endblock %}""",

}

for filepath, content in files.items():
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Created: {filepath}")

print("\nFinal polish applied!")