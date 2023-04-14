# template strings
# campaign
campaign_list_item = """
<h3>
  <a href="{{ url_for('api.timeline', id=campaign.id) }}">
    {{campaign.title}}
  </a>
  <span 
      hx-delete="{{ url_for('api.campaign', id=campaign.id) }}" 
      hx-swap="delete" >
    Delete
  </span>"
</h3>
"""
campaign_list_item_deleted = """
<p>deleted</p>"
"""

# timeline
timeline_note = """
<div class="timeline-note">
  <p>
    <span>{{note.time}}:</span>
    <span>{{note.text}}</span>
  </p>
  <p>
    {{note.author.email}}
  </p>
</div>
"""
