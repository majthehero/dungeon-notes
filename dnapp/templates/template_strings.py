# template strings
# campaign
dms_campaign_item = """
<div id="c_id_{{ campaign.id }}">
  <h3>
    <a href="{{ url_for('timeline_bp.timeline', id=campaign.id) }}">
      {{ campaign.title }}
    </a>
  </h3>
  <span hx-delete="{{ url_for('campaign_bp.campaign', id=campaign.id, cmd="dm-delete") }}" 
        hx-swap="outerHTML"
        hx-target="#c_id_{{ campaign.id }}">
    Delete campaign
  </span>
</div>
"""
plays_campaign_item = """
<div id="c_id_{{ campaign.id }}">
  <h3>
    <a href="{{ url_for('timeline_bp.timeline', id=campaign.id) }}">
      {{ campaign.title }}
    </a>
  </h3>
  <span hx-delete="{{ url_for('campaign_bp.campaign', id=campaign.id, cmd="player-leave") }}" 
        hx-swap="outerHTML"
        hx-target="#c_id_{{ campaign.id }}">
    Leave campaign
  </span>
</div>
"""
campaign_deleted = """
<p>deleted</p>
"""
campaign_left = """
<p>left</p>
"""

# timeline
timeline_note = """
<div class="timeline-note">
  <span class="note-time">{{note.time}}:</span>
  <span class="note-text">{{note.text}}</span>
  <p class="author">{{note.author.email}}</p>
  <hr />
</div>
"""


add_location_form = """
<div id="location-form" class="column timeline">
  <label for="name"> name </label>
  <input type="text" />
  <label for="description" /> description </label>
  <textarea type="text" name="description"></textarea>
  
  <input name="x" value="{{x}}" hidden="True"></input>
  <input name="y" value="{{y}}" hidden="True"></input>
  <input name="scale" value="{{scale}}" hidden="True"></input>
  <input name="campaign_id" value="{{campaign_id}}" hidden="True"></input>
  <input type="button" hx-post="https://dungeon-notes.herokuapp.com/location/add/2"
      hx-target="#location-form"
      hx-swap="delete">Button</submit>
</div>
"""
