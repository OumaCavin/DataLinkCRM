#!/bin/bash

# Create basic templates for all apps
for app in projects subscriptions payments communications analytics settings widgets schedulecal maps reports; do
cat > templates/${app}/index.html << 'EOF'
{% extends 'layouts/base.html' %}

{% block title %}{{ title }} - {{ SITE_NAME|default:"DataLinkCRM" }}{% endblock %}

{% block content %}
<div class="row">
    <div class="col-12">
        <div class="d-flex justify-content-between align-items-center mb-4">
            <h1 class="h3 mb-0">{{ title }}</h1>
        </div>
        
        <div class="card">
            <div class="card-body text-center py-5">
                <i class="fas fa-tools fa-3x text-muted mb-3"></i>
                <h4>Coming Soon</h4>
                <p class="text-muted">This section is under development.</p>
                <a href="{% url 'dashboard:index' %}" class="btn btn-primary">
                    <i class="fas fa-arrow-left me-2"></i>Back to Dashboard
                </a>
            </div>
        </div>
    </div>
</div>
{% endblock %}
EOF
done