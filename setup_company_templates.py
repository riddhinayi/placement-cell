import os

files = {

"app/templates/company/dashboard.html": """{% extends 'base.html' %}
{% block content %}
<h2 class="fw-bold mb-4">Company Dashboard</h2>

{% if not profile.is_approved %}
<div class="alert alert-warning">
  Your company is <strong>pending admin approval</strong>.
  You cannot post job drives until approved.
</div>
{% endif %}

<div class="row g-3 mb-4">
  <div class="col-md-3">
    <div class="card text-white bg-primary shadow-sm">
      <div class="card-body text-center">
        <h3 class="fw-bold">{{ stats.total_drives }}</h3>
        <p class="mb-0">Total Drives</p>
      </div>
    </div>
  </div>
  <div class="col-md-3">
    <div class="card text-white bg-success shadow-sm">
      <div class="card-body text-center">
        <h3 class="fw-bold">{{ stats.approved_drives }}</h3>
        <p class="mb-0">Approved Drives</p>
      </div>
    </div>
  </div>
  <div class="col-md-3">
    <div class="card text-white bg-info shadow-sm">
      <div class="card-body text-center">
        <h3 class="fw-bold">{{ stats.total_applications }}</h3>
        <p class="mb-0">Total Applicants</p>
      </div>
    </div>
  </div>
  <div class="col-md-3">
    <div class="card text-white bg-warning shadow-sm">
      <div class="card-body text-center">
        <h3 class="fw-bold">{{ stats.total_selected }}</h3>
        <p class="mb-0">Selected</p>
      </div>
    </div>
  </div>
</div>

<div class="row g-3">
  <div class="col-md-4">
    <div class="card shadow-sm h-100">
      <div class="card-header fw-bold">Company Profile</div>
      <div class="card-body">
        <p><strong>Name:</strong> {{ profile.company_name }}</p>
        <p><strong>Industry:</strong> {{ profile.industry or '-' }}</p>
        <p><strong>Location:</strong> {{ profile.location or '-' }}</p>
        <p><strong>Website:</strong>
          {% if profile.website %}
            <a href="{{ profile.website }}" target="_blank">{{ profile.website }}</a>
          {% else %}-{% endif %}
        </p>
        <p><strong>Status:</strong>
          {% if profile.is_approved %}
            <span class="badge bg-success">Approved</span>
          {% else %}
            <span class="badge bg-warning text-dark">Pending</span>
          {% endif %}
        </p>
        <a href="{{ url_for('company.profile') }}"
           class="btn btn-outline-primary btn-sm">Edit Profile</a>
      </div>
    </div>
  </div>

  <div class="col-md-8">
    <div class="card shadow-sm mb-3">
      <div class="card-header fw-bold d-flex justify-content-between">
        My Job Drives
        <div>
          <a href="{{ url_for('company.my_drives') }}"
             class="btn btn-sm btn-outline-secondary me-1">View All</a>
          {% if profile.is_approved %}
          <a href="{{ url_for('company.new_drive') }}"
             class="btn btn-sm btn-success">+ Post Drive</a>
          {% endif %}
        </div>
      </div>
      <div class="card-body p-0">
        <table class="table table-hover mb-0">
          <thead class="table-light">
            <tr><th>Title</th><th>Package</th><th>Applicants</th><th>Status</th></tr>
          </thead>
          <tbody>
            {% for d in drives[:5] %}
            <tr>
              <td><a href="{{ url_for('company.applicants', drive_id=d.id) }}">{{ d.title }}</a></td>
              <td>{{ d.package }} LPA</td>
              <td>{{ d.applications|length }}</td>
              <td>{% if d.is_approved %}<span class="badge bg-success">Approved</span>
                  {% else %}<span class="badge bg-warning text-dark">Pending</span>{% endif %}</td>
            </tr>
            {% else %}
            <tr><td colspan="4" class="text-center text-muted">No drives posted yet</td></tr>
            {% endfor %}
          </tbody>
        </table>
      </div>
    </div>

    <div class="card shadow-sm">
      <div class="card-header fw-bold">Recent Applicants</div>
      <div class="card-body p-0">
        <table class="table table-hover mb-0">
          <thead class="table-light">
            <tr><th>Student</th><th>Drive</th><th>CGPA</th><th>Status</th></tr>
          </thead>
          <tbody>
            {% for a in recent_apps %}
            <tr>
              <td>{{ a.student.user.name }}</td>
              <td>{{ a.job_drive.title }}</td>
              <td>{{ a.student.cgpa }}</td>
              <td><span class="badge
                {% if a.status=='selected' %}bg-success
                {% elif a.status=='rejected' %}bg-danger
                {% elif a.status=='shortlisted' %}bg-info
                {% elif a.status=='interview' %}bg-primary
                {% else %}bg-secondary{% endif %}">{{ a.status }}</span></td>
            </tr>
            {% else %}
            <tr><td colspan="4" class="text-center text-muted">No applicants yet</td></tr>
            {% endfor %}
          </tbody>
        </table>
      </div>
    </div>
  </div>
</div>
{% endblock %}""",

"app/templates/company/profile.html": """{% extends 'base.html' %}
{% block content %}
<div class="row justify-content-center">
  <div class="col-md-7">
    <div class="card shadow-sm">
      <div class="card-header fw-bold">Edit Company Profile</div>
      <div class="card-body">
        <form method="POST">
          {{ form.hidden_tag() }}
          <div class="mb-3">
            {{ form.company_name.label(class="form-label") }}
            {{ form.company_name(class="form-control") }}
          </div>
          <div class="mb-3">
            {{ form.industry.label(class="form-label") }}
            {{ form.industry(class="form-select") }}
          </div>
          <div class="mb-3">
            {{ form.location.label(class="form-label") }}
            {{ form.location(class="form-control", placeholder="City, Country") }}
          </div>
          <div class="mb-3">
            {{ form.website.label(class="form-label") }}
            {{ form.website(class="form-control", placeholder="https://company.com") }}
          </div>
          <div class="mb-3">
            {{ form.description.label(class="form-label") }}
            {{ form.description(class="form-control", rows=4,
               placeholder="Tell students about your company...") }}
          </div>
          {{ form.submit(class="btn btn-primary w-100") }}
        </form>
      </div>
    </div>
  </div>
</div>
{% endblock %}""",

"app/templates/company/new_drive.html": """{% extends 'base.html' %}
{% block content %}
<div class="row justify-content-center">
  <div class="col-md-8">
    <div class="card shadow-sm">
      <div class="card-header fw-bold">Post a New Job Drive</div>
      <div class="card-body">
        <form method="POST">
          {{ form.hidden_tag() }}
          <div class="row">
            <div class="col-md-8 mb-3">
              {{ form.title.label(class="form-label") }}
              {{ form.title(class="form-control", placeholder="e.g. Software Engineer") }}
            </div>
            <div class="col-md-4 mb-3">
              {{ form.job_type.label(class="form-label") }}
              {{ form.job_type(class="form-select") }}
            </div>
          </div>
          <div class="mb-3">
            {{ form.description.label(class="form-label") }}
            {{ form.description(class="form-control", rows=4,
               placeholder="Job responsibilities, requirements...") }}
          </div>
          <div class="row">
            <div class="col-md-6 mb-3">
              {{ form.package.label(class="form-label") }}
              {{ form.package(class="form-control", placeholder="e.g. 6.5") }}
            </div>
            <div class="col-md-6 mb-3">
              {{ form.location.label(class="form-label") }}
              {{ form.location(class="form-control", placeholder="e.g. Bangalore") }}
            </div>
          </div>
          <hr/>
          <h6 class="fw-bold mb-3">Eligibility Criteria</h6>
          <div class="row">
            <div class="col-md-4 mb-3">
              {{ form.min_cgpa.label(class="form-label") }}
              {{ form.min_cgpa(class="form-control", placeholder="e.g. 7.0") }}
            </div>
            <div class="col-md-4 mb-3">
              {{ form.max_backlogs.label(class="form-label") }}
              {{ form.max_backlogs(class="form-control", placeholder="e.g. 0") }}
            </div>
            <div class="col-md-4 mb-3">
              {{ form.allowed_branches.label(class="form-label") }}
              {{ form.allowed_branches(class="form-control", placeholder="CSE,IT,ECE") }}
            </div>
          </div>
          <hr/>
          <h6 class="fw-bold mb-3">Drive Schedule</h6>
          <div class="row">
            <div class="col-md-6 mb-3">
              {{ form.apply_deadline.label(class="form-label") }}
              {{ form.apply_deadline(class="form-control", placeholder="2025-12-31") }}
            </div>
            <div class="col-md-6 mb-3">
              {{ form.drive_date.label(class="form-label") }}
              {{ form.drive_date(class="form-control", placeholder="2026-01-15") }}
            </div>
          </div>
          <div class="d-flex gap-2">
            {{ form.submit(class="btn btn-success") }}
            <a href="{{ url_for('company.my_drives') }}"
               class="btn btn-outline-secondary">Cancel</a>
          </div>
        </form>
      </div>
    </div>
  </div>
</div>
{% endblock %}""",

"app/templates/company/drives.html": """{% extends 'base.html' %}
{% block content %}
<div class="d-flex justify-content-between align-items-center mb-4">
  <h2 class="fw-bold">My Job Drives</h2>
  <a href="{{ url_for('company.new_drive') }}" class="btn btn-success">+ Post New Drive</a>
</div>
<div class="card shadow-sm">
  <div class="card-body p-0">
    <table class="table table-hover mb-0">
      <thead class="table-dark">
        <tr>
          <th>#</th><th>Title</th><th>Package</th><th>Deadline</th>
          <th>Applicants</th><th>Status</th><th>Actions</th>
        </tr>
      </thead>
      <tbody>
        {% for d in drives %}
        <tr>
          <td>{{ loop.index }}</td>
          <td>{{ d.title }}</td>
          <td>{{ d.package }} LPA</td>
          <td>{{ d.apply_deadline.strftime('%d %b %Y') if d.apply_deadline else 'Open' }}</td>
          <td>
            <a href="{{ url_for('company.applicants', drive_id=d.id) }}">
              {{ d.applications|length }} applicants
            </a>
          </td>
          <td>
            {% if d.is_approved %}
              <span class="badge bg-success">Approved</span>
            {% else %}
              <span class="badge bg-warning text-dark">Pending</span>
            {% endif %}
          </td>
          <td>
            <a href="{{ url_for('company.applicants', drive_id=d.id) }}"
               class="btn btn-info btn-sm">View Applicants</a>
            <a href="{{ url_for('company.delete_drive', id=d.id) }}"
               class="btn btn-danger btn-sm"
               onclick="return confirm('Delete this drive?')">Delete</a>
          </td>
        </tr>
        {% else %}
        <tr><td colspan="7" class="text-center text-muted">No drives posted yet</td></tr>
        {% endfor %}
      </tbody>
    </table>
  </div>
</div>
{% endblock %}""",

"app/templates/company/applicants.html": """{% extends 'base.html' %}
{% block content %}
<div class="d-flex justify-content-between align-items-center mb-4">
  <div>
    <h2 class="fw-bold mb-0">Applicants</h2>
    <small class="text-muted">Drive: {{ drive.title }} &mdash; {{ drive.package }} LPA</small>
  </div>
  <a href="{{ url_for('company.my_drives') }}" class="btn btn-outline-secondary btn-sm">Back</a>
</div>
<div class="card shadow-sm">
  <div class="card-body p-0">
    <table class="table table-hover mb-0">
      <thead class="table-dark">
        <tr>
          <th>#</th><th>Name</th><th>Branch</th><th>CGPA</th>
          <th>Backlogs</th><th>Skills</th><th>Resume</th><th>Status</th><th>Update</th>
        </tr>
      </thead>
      <tbody>
        {% for a in applications %}
        <tr>
          <td>{{ loop.index }}</td>
          <td>{{ a.student.user.name }}</td>
          <td>{{ a.student.branch }}</td>
          <td>{{ a.student.cgpa }}</td>
          <td>{{ a.student.backlogs }}</td>
          <td>
            <small>{{ a.student.skills or '-' }}</small>
          </td>
          <td>
            {% if a.student.resume_url %}
              <a href="{{ a.student.resume_url }}" target="_blank"
                 class="btn btn-outline-primary btn-sm">View</a>
            {% else %}
              <span class="text-muted">-</span>
            {% endif %}
          </td>
          <td>
            <span class="badge
              {% if a.status=='selected' %}bg-success
              {% elif a.status=='rejected' %}bg-danger
              {% elif a.status=='shortlisted' %}bg-info
              {% elif a.status=='interview' %}bg-primary
              {% else %}bg-secondary{% endif %}">
              {{ a.status }}
            </span>
          </td>
          <td>
            <form method="POST"
                  action="{{ url_for('company.update_status', app_id=a.id) }}"
                  class="d-flex gap-1">
              <select name="status" class="form-select form-select-sm" style="width:130px">
                <option value="applied"     {% if a.status=='applied'     %}selected{% endif %}>Applied</option>
                <option value="shortlisted" {% if a.status=='shortlisted' %}selected{% endif %}>Shortlisted</option>
                <option value="interview"   {% if a.status=='interview'   %}selected{% endif %}>Interview</option>
                <option value="selected"    {% if a.status=='selected'    %}selected{% endif %}>Selected</option>
                <option value="rejected"    {% if a.status=='rejected'    %}selected{% endif %}>Rejected</option>
              </select>
              <button type="submit" class="btn btn-primary btn-sm">Update</button>
            </form>
          </td>
        </tr>
        {% else %}
        <tr>
          <td colspan="9" class="text-center text-muted py-3">No applicants yet</td>
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

print("\nAll company templates created!")