import os

files = {

"app/templates/admin/dashboard.html": """{% extends 'base.html' %}
{% block content %}
<h2 class="fw-bold mb-4">Admin Dashboard</h2>

<div class="row g-3 mb-4">
  <div class="col-md-3">
    <div class="card text-white bg-primary shadow-sm">
      <div class="card-body text-center">
        <h3 class="fw-bold">{{ stats.total_students }}</h3>
        <p class="mb-0">Total Students</p>
      </div>
    </div>
  </div>
  <div class="col-md-3">
    <div class="card text-white bg-success shadow-sm">
      <div class="card-body text-center">
        <h3 class="fw-bold">{{ stats.total_placed }}</h3>
        <p class="mb-0">Students Placed</p>
      </div>
    </div>
  </div>
  <div class="col-md-3">
    <div class="card text-white bg-warning shadow-sm">
      <div class="card-body text-center">
        <h3 class="fw-bold">{{ stats.total_companies }}</h3>
        <p class="mb-0">Companies</p>
      </div>
    </div>
  </div>
  <div class="col-md-3">
    <div class="card text-white bg-info shadow-sm">
      <div class="card-body text-center">
        <h3 class="fw-bold">{{ stats.total_drives }}</h3>
        <p class="mb-0">Job Drives</p>
      </div>
    </div>
  </div>
</div>

<div class="row g-3 mb-4">
  <div class="col-md-4">
    <div class="card border-danger shadow-sm">
      <div class="card-body text-center">
        <h4 class="text-danger fw-bold">{{ stats.pending_companies }}</h4>
        <p class="mb-1">Pending Company Approvals</p>
        <a href="{{ url_for('admin.companies') }}" class="btn btn-sm btn-outline-danger">Review</a>
      </div>
    </div>
  </div>
  <div class="col-md-4">
    <div class="card border-warning shadow-sm">
      <div class="card-body text-center">
        <h4 class="text-warning fw-bold">{{ stats.pending_drives }}</h4>
        <p class="mb-1">Pending Drive Approvals</p>
        <a href="{{ url_for('admin.drives') }}" class="btn btn-sm btn-outline-warning">Review</a>
      </div>
    </div>
  </div>
  <div class="col-md-4">
    <div class="card border-info shadow-sm">
      <div class="card-body text-center">
        <h4 class="text-info fw-bold">{{ stats.total_applications }}</h4>
        <p class="mb-1">Total Applications</p>
        <a href="{{ url_for('admin.applications') }}" class="btn btn-sm btn-outline-info">View All</a>
      </div>
    </div>
  </div>
</div>

<div class="row g-3">
  <div class="col-md-6">
    <div class="card shadow-sm">
      <div class="card-header fw-bold">Recent Job Drives</div>
      <div class="card-body p-0">
        <table class="table table-hover mb-0">
          <thead class="table-light">
            <tr><th>Title</th><th>Company</th><th>Status</th></tr>
          </thead>
          <tbody>
            {% for drive in recent_drives %}
            <tr>
              <td>{{ drive.title }}</td>
              <td>{{ drive.company.company_name }}</td>
              <td>
                {% if drive.is_approved %}
                  <span class="badge bg-success">Approved</span>
                {% else %}
                  <span class="badge bg-warning text-dark">Pending</span>
                {% endif %}
              </td>
            </tr>
            {% else %}
            <tr><td colspan="3" class="text-center text-muted">No drives yet</td></tr>
            {% endfor %}
          </tbody>
        </table>
      </div>
    </div>
  </div>
  <div class="col-md-6">
    <div class="card shadow-sm">
      <div class="card-header fw-bold">Recent Applications</div>
      <div class="card-body p-0">
        <table class="table table-hover mb-0">
          <thead class="table-light">
            <tr><th>Student</th><th>Drive</th><th>Status</th></tr>
          </thead>
          <tbody>
            {% for app in recent_applications %}
            <tr>
              <td>{{ app.student.user.name }}</td>
              <td>{{ app.job_drive.title }}</td>
              <td>
                <span class="badge
                  {% if app.status == 'selected' %}bg-success
                  {% elif app.status == 'rejected' %}bg-danger
                  {% elif app.status == 'shortlisted' %}bg-info
                  {% else %}bg-secondary{% endif %}">
                  {{ app.status }}
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

"app/templates/admin/students.html": """{% extends 'base.html' %}
{% block content %}
<div class="d-flex justify-content-between align-items-center mb-4">
  <h2 class="fw-bold">All Students</h2>
  <a href="{{ url_for('admin.dashboard') }}" class="btn btn-outline-secondary btn-sm">Back</a>
</div>
<div class="card shadow-sm">
  <div class="card-body p-0">
    <table class="table table-hover mb-0">
      <thead class="table-dark">
        <tr>
          <th>#</th><th>Name</th><th>Email</th><th>Roll No</th>
          <th>Branch</th><th>CGPA</th><th>Placed</th><th>Action</th>
        </tr>
      </thead>
      <tbody>
        {% for s in students %}
        <tr>
          <td>{{ loop.index }}</td>
          <td>{{ s.user.name }}</td>
          <td>{{ s.user.email }}</td>
          <td>{{ s.roll_number }}</td>
          <td>{{ s.branch }}</td>
          <td>{{ s.cgpa }}</td>
          <td>
            {% if s.is_placed %}
              <span class="badge bg-success">Yes</span>
            {% else %}
              <span class="badge bg-secondary">No</span>
            {% endif %}
          </td>
          <td>
            <a href="{{ url_for('admin.delete_student', id=s.id) }}"
               class="btn btn-danger btn-sm"
               onclick="return confirm('Delete this student?')">Delete</a>
          </td>
        </tr>
        {% else %}
        <tr><td colspan="8" class="text-center text-muted">No students registered yet</td></tr>
        {% endfor %}
      </tbody>
    </table>
  </div>
</div>
{% endblock %}""",

"app/templates/admin/companies.html": """{% extends 'base.html' %}
{% block content %}
<div class="d-flex justify-content-between align-items-center mb-4">
  <h2 class="fw-bold">All Companies</h2>
  <a href="{{ url_for('admin.dashboard') }}" class="btn btn-outline-secondary btn-sm">Back</a>
</div>
<div class="card shadow-sm">
  <div class="card-body p-0">
    <table class="table table-hover mb-0">
      <thead class="table-dark">
        <tr><th>#</th><th>Company</th><th>Industry</th><th>Location</th><th>Status</th><th>Actions</th></tr>
      </thead>
      <tbody>
        {% for c in companies %}
        <tr>
          <td>{{ loop.index }}</td>
          <td>{{ c.company_name }}</td>
          <td>{{ c.industry or '-' }}</td>
          <td>{{ c.location or '-' }}</td>
          <td>
            {% if c.is_approved %}
              <span class="badge bg-success">Approved</span>
            {% else %}
              <span class="badge bg-warning text-dark">Pending</span>
            {% endif %}
          </td>
          <td>
            {% if not c.is_approved %}
              <a href="{{ url_for('admin.approve_company', id=c.id) }}"
                 class="btn btn-success btn-sm">Approve</a>
            {% endif %}
            <a href="{{ url_for('admin.delete_company', id=c.id) }}"
               class="btn btn-danger btn-sm"
               onclick="return confirm('Remove this company?')">Remove</a>
          </td>
        </tr>
        {% else %}
        <tr><td colspan="6" class="text-center text-muted">No companies registered yet</td></tr>
        {% endfor %}
      </tbody>
    </table>
  </div>
</div>
{% endblock %}""",

"app/templates/admin/drives.html": """{% extends 'base.html' %}
{% block content %}
<div class="d-flex justify-content-between align-items-center mb-4">
  <h2 class="fw-bold">All Job Drives</h2>
  <a href="{{ url_for('admin.dashboard') }}" class="btn btn-outline-secondary btn-sm">Back</a>
</div>
<div class="card shadow-sm">
  <div class="card-body p-0">
    <table class="table table-hover mb-0">
      <thead class="table-dark">
        <tr><th>#</th><th>Title</th><th>Company</th><th>Package</th><th>Deadline</th><th>Status</th><th>Actions</th></tr>
      </thead>
      <tbody>
        {% for d in drives %}
        <tr>
          <td>{{ loop.index }}</td>
          <td>{{ d.title }}</td>
          <td>{{ d.company.company_name }}</td>
          <td>{{ d.package }} LPA</td>
          <td>{{ d.apply_deadline.strftime('%d %b %Y') if d.apply_deadline else '-' }}</td>
          <td>
            {% if d.is_approved %}
              <span class="badge bg-success">Approved</span>
            {% else %}
              <span class="badge bg-warning text-dark">Pending</span>
            {% endif %}
          </td>
          <td>
            {% if not d.is_approved %}
              <a href="{{ url_for('admin.approve_drive', id=d.id) }}"
                 class="btn btn-success btn-sm">Approve</a>
            {% endif %}
            <a href="{{ url_for('admin.delete_drive', id=d.id) }}"
               class="btn btn-danger btn-sm"
               onclick="return confirm('Delete this drive?')">Delete</a>
          </td>
        </tr>
        {% else %}
        <tr><td colspan="7" class="text-center text-muted">No job drives yet</td></tr>
        {% endfor %}
      </tbody>
    </table>
  </div>
</div>
{% endblock %}""",

"app/templates/admin/applications.html": """{% extends 'base.html' %}
{% block content %}
<div class="d-flex justify-content-between align-items-center mb-4">
  <h2 class="fw-bold">All Applications</h2>
  <a href="{{ url_for('admin.dashboard') }}" class="btn btn-outline-secondary btn-sm">Back</a>
</div>
<div class="card shadow-sm">
  <div class="card-body p-0">
    <table class="table table-hover mb-0">
      <thead class="table-dark">
        <tr><th>#</th><th>Student</th><th>Drive</th><th>Applied On</th><th>Status</th><th>Update</th></tr>
      </thead>
      <tbody>
        {% for a in applications %}
        <tr>
          <td>{{ loop.index }}</td>
          <td>{{ a.student.user.name }}</td>
          <td>{{ a.job_drive.title }}</td>
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
            <form method="POST"
                  action="{{ url_for('admin.update_application', id=a.id) }}"
                  class="d-flex gap-1">
              <select name="status" class="form-select form-select-sm" style="width:130px">
                <option value="applied"     {% if a.status=='applied'      %}selected{% endif %}>Applied</option>
                <option value="shortlisted" {% if a.status=='shortlisted'  %}selected{% endif %}>Shortlisted</option>
                <option value="interview"   {% if a.status=='interview'    %}selected{% endif %}>Interview</option>
                <option value="selected"    {% if a.status=='selected'     %}selected{% endif %}>Selected</option>
                <option value="rejected"    {% if a.status=='rejected'     %}selected{% endif %}>Rejected</option>
              </select>
              <button type="submit" class="btn btn-primary btn-sm">Update</button>
            </form>
          </td>
        </tr>
        {% else %}
        <tr><td colspan="6" class="text-center text-muted">No applications yet</td></tr>
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

print("\nAll admin templates created!")