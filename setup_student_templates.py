import os

files = {

"app/templates/student/dashboard.html": """{% extends 'base.html' %}
{% block content %}
<h2 class="fw-bold mb-4">Student Dashboard</h2>

{% if not profile or profile.branch == 'Not Set' %}
<div class="alert alert-warning">
  Your profile is incomplete!
  <a href="{{ url_for('student.profile') }}" class="alert-link">Complete your profile</a>
  to apply for job drives.
</div>
{% endif %}

<div class="row g-3 mb-4">
  <div class="col-md-3">
    <div class="card text-white bg-primary shadow-sm">
      <div class="card-body text-center">
        <h3 class="fw-bold">{{ stats.total_applied }}</h3>
        <p class="mb-0">Applied</p>
      </div>
    </div>
  </div>
  <div class="col-md-3">
    <div class="card text-white bg-info shadow-sm">
      <div class="card-body text-center">
        <h3 class="fw-bold">{{ stats.shortlisted }}</h3>
        <p class="mb-0">Shortlisted</p>
      </div>
    </div>
  </div>
  <div class="col-md-3">
    <div class="card text-white bg-warning shadow-sm">
      <div class="card-body text-center">
        <h3 class="fw-bold">{{ stats.interviews }}</h3>
        <p class="mb-0">Interviews</p>
      </div>
    </div>
  </div>
  <div class="col-md-3">
    <div class="card text-white bg-success shadow-sm">
      <div class="card-body text-center">
        <h3 class="fw-bold">{{ stats.selected }}</h3>
        <p class="mb-0">Selected</p>
      </div>
    </div>
  </div>
</div>

<div class="row g-3">
  <div class="col-md-4">
    <div class="card shadow-sm h-100">
      <div class="card-header fw-bold">My Profile</div>
      <div class="card-body">
        {% if profile %}
        <p><strong>Roll No:</strong> {{ profile.roll_number }}</p>
        <p><strong>Branch:</strong> {{ profile.branch }}</p>
        <p><strong>CGPA:</strong> {{ profile.cgpa }}</p>
        <p><strong>Backlogs:</strong> {{ profile.backlogs }}</p>
        <p><strong>Phone:</strong> {{ profile.phone or '-' }}</p>
        <p><strong>Status:</strong>
          {% if profile.is_placed %}
            <span class="badge bg-success">Placed</span>
          {% else %}
            <span class="badge bg-secondary">Not Placed</span>
          {% endif %}
        </p>
        {% endif %}
        <a href="{{ url_for('student.profile') }}" class="btn btn-outline-primary btn-sm">Edit Profile</a>
      </div>
    </div>
  </div>

  <div class="col-md-8">
    <div class="card shadow-sm">
      <div class="card-header fw-bold d-flex justify-content-between">
        Open Job Drives
        <a href="{{ url_for('student.drives') }}" class="btn btn-sm btn-outline-primary">View All</a>
      </div>
      <div class="card-body p-0">
        <table class="table table-hover mb-0">
          <thead class="table-light">
            <tr><th>Company</th><th>Role</th><th>Package</th><th>Deadline</th></tr>
          </thead>
          <tbody>
            {% for d in open_drives %}
            <tr>
              <td>{{ d.company.company_name }}</td>
              <td>{{ d.title }}</td>
              <td>{{ d.package }} LPA</td>
              <td>{{ d.apply_deadline.strftime('%d %b %Y') if d.apply_deadline else 'Open' }}</td>
            </tr>
            {% else %}
            <tr><td colspan="4" class="text-center text-muted">No open drives</td></tr>
            {% endfor %}
          </tbody>
        </table>
      </div>
    </div>

    <div class="card shadow-sm mt-3">
      <div class="card-header fw-bold d-flex justify-content-between">
        My Recent Applications
        <a href="{{ url_for('student.my_applications') }}" class="btn btn-sm btn-outline-secondary">View All</a>
      </div>
      <div class="card-body p-0">
        <table class="table table-hover mb-0">
          <thead class="table-light">
            <tr><th>Company</th><th>Role</th><th>Status</th></tr>
          </thead>
          <tbody>
            {% for a in applications[:4] %}
            <tr>
              <td>{{ a.job_drive.company.company_name }}</td>
              <td>{{ a.job_drive.title }}</td>
              <td>
                <span class="badge
                  {% if a.status == 'selected' %}bg-success
                  {% elif a.status == 'rejected' %}bg-danger
                  {% elif a.status == 'shortlisted' %}bg-info
                  {% elif a.status == 'interview' %}bg-primary
                  {% else %}bg-secondary{% endif %}">
                  {{ a.status }}
                </span>
              </td>
            </tr>
            {% else %}
            <tr><td colspan="3" class="text-center text-muted">No applications yet</td></tr>
            {% endfor %}
          </tbody>
        </table>
      </div>
    </div>
  </div>
</div>
{% endblock %}""",

"app/templates/student/profile.html": """{% extends 'base.html' %}
{% block content %}
<div class="row justify-content-center">
  <div class="col-md-7">
    <div class="card shadow-sm">
      <div class="card-header fw-bold">Edit My Profile</div>
      <div class="card-body">
        <form method="POST">
          {{ form.hidden_tag() }}
          <div class="mb-3">
            {{ form.roll_number.label(class="form-label") }}
            {{ form.roll_number(class="form-control") }}
          </div>
          <div class="mb-3">
            {{ form.branch.label(class="form-label") }}
            {{ form.branch(class="form-select") }}
          </div>
          <div class="row">
            <div class="col-md-6 mb-3">
              {{ form.cgpa.label(class="form-label") }}
              {{ form.cgpa(class="form-control") }}
            </div>
            <div class="col-md-6 mb-3">
              {{ form.backlogs.label(class="form-label") }}
              {{ form.backlogs(class="form-control") }}
            </div>
          </div>
          <div class="mb-3">
            {{ form.phone.label(class="form-label") }}
            {{ form.phone(class="form-control") }}
          </div>
          <div class="mb-3">
            {{ form.skills.label(class="form-label") }}
            {{ form.skills(class="form-control", rows=3,
               placeholder="Python, Flask, SQL, JavaScript...") }}
          </div>
          <div class="mb-3">
            {{ form.resume_url.label(class="form-label") }}
            {{ form.resume_url(class="form-control",
               placeholder="https://drive.google.com/...") }}
          </div>
          {{ form.submit(class="btn btn-primary w-100") }}
        </form>
      </div>
    </div>
  </div>
</div>
{% endblock %}""",

"app/templates/student/drives.html": """{% extends 'base.html' %}
{% block content %}
<h2 class="fw-bold mb-4">Available Job Drives</h2>
<div class="row g-3">
  {% for drive in drives %}
  <div class="col-md-6">
    <div class="card shadow-sm h-100">
      <div class="card-header d-flex justify-content-between align-items-center">
        <span class="fw-bold">{{ drive.company.company_name }}</span>
        <span class="badge bg-info text-dark">{{ drive.job_type or 'Full-time' }}</span>
      </div>
      <div class="card-body">
        <h5 class="card-title">{{ drive.title }}</h5>
        <p class="text-muted small">{{ drive.description or 'No description provided.' }}</p>
        <div class="row text-center mb-3">
          <div class="col">
            <strong>{{ drive.package }} LPA</strong><br>
            <small class="text-muted">Package</small>
          </div>
          <div class="col">
            <strong>{{ drive.min_cgpa }}</strong><br>
            <small class="text-muted">Min CGPA</small>
          </div>
          <div class="col">
            <strong>{{ drive.max_backlogs }}</strong><br>
            <small class="text-muted">Max Backlogs</small>
          </div>
        </div>
        <p class="small mb-1">
          <strong>Branches:</strong> {{ drive.allowed_branches or 'All' }}
        </p>
        <p class="small mb-3">
          <strong>Deadline:</strong>
          {{ drive.apply_deadline.strftime('%d %b %Y') if drive.apply_deadline else 'Open' }}
        </p>

        {% if drive.id in applied_ids %}
          <button class="btn btn-secondary w-100" disabled>Already Applied</button>
        {% elif profile and profile.is_placed %}
          <button class="btn btn-secondary w-100" disabled>You are already placed</button>
        {% else %}
          <a href="{{ url_for('student.apply', drive_id=drive.id) }}"
             class="btn btn-success w-100">Apply Now</a>
        {% endif %}
      </div>
    </div>
  </div>
  {% else %}
  <div class="col-12">
    <div class="alert alert-info">No job drives available right now. Check back later!</div>
  </div>
  {% endfor %}
</div>
{% endblock %}""",

"app/templates/student/applications.html": """{% extends 'base.html' %}
{% block content %}
<div class="d-flex justify-content-between align-items-center mb-4">
  <h2 class="fw-bold">My Applications</h2>
  <a href="{{ url_for('student.dashboard') }}" class="btn btn-outline-secondary btn-sm">Back</a>
</div>
<div class="card shadow-sm">
  <div class="card-body p-0">
    <table class="table table-hover mb-0">
      <thead class="table-dark">
        <tr>
          <th>#</th><th>Company</th><th>Role</th><th>Package</th>
          <th>Applied On</th><th>Status</th><th>Interview</th>
        </tr>
      </thead>
      <tbody>
        {% for a in applications %}
        <tr>
          <td>{{ loop.index }}</td>
          <td>{{ a.job_drive.company.company_name }}</td>
          <td>{{ a.job_drive.title }}</td>
          <td>{{ a.job_drive.package }} LPA</td>
          <td>{{ a.applied_at.strftime('%d %b %Y') }}</td>
          <td>
            <span class="badge
              {% if a.status == 'selected' %}bg-success
              {% elif a.status == 'rejected' %}bg-danger
              {% elif a.status == 'shortlisted' %}bg-info
              {% elif a.status == 'interview' %}bg-primary
              {% else %}bg-secondary{% endif %}">
              {{ a.status }}
            </span>
          </td>
          <td>
            {% if a.interview_date %}
              {{ a.interview_date.strftime('%d %b %Y') }}<br>
              <small class="text-muted">{{ a.interview_round }}</small>
            {% else %}
              <span class="text-muted">-</span>
            {% endif %}
          </td>
        </tr>
        {% else %}
        <tr>
          <td colspan="7" class="text-center text-muted py-3">
            You haven't applied to any drives yet.
            <a href="{{ url_for('student.drives') }}">Browse drives</a>
          </td>
        </tr>
        {% endfor %}
      </tbody>
    </table>
  </div>
</div>
{% endblock %}"""
}

for filepath, content in files.items():
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Created: {filepath}")

print("\nAll student templates created!")