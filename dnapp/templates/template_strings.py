# template strings
# campaign
campaign_list_item = """
<div>
  <h3>
    <a href="{{ url_for('api.timeline', id=campaign.id) }}">
      {{campaign.title}}
    </a>
  </h3>
  <span class="campaign-delete">
    <a 
      hx-delete="{{ url_for('api.campaign', id=campaign.id) }}" 
      hx-swap="delete">
    Delete
    </a>
  </span>
</div>
"""
campaign_list_item_deleted = """
<p>deleted</p>"
"""

# timeline
timeline_note = """
<div class="timeline-note">
  <span class="note-time">{{note.time}}:</span>
  <span class="note-text">{{note.text}}</span>
  <p class="author">
    {{note.author.email}}
  </p>
</div>
"""
