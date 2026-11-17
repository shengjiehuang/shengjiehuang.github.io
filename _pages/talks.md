---
layout: page
permalink: /talks/
title: Talks
description: Selected talks, newest first.
nav: true
nav_order: 4
---

<div class="publications talks">
<ol class="bibliography">
{% for talk in site.data.talks %}
  <li>
    <div class="row">
      <div class="col-sm-2 abbr"><abbr class="badge rounded w-100">{{ talk.date | split: " " | last }}</abbr></div>
      <div class="col-sm-10">
        <div class="title">{{ talk.title }}</div>
        <div class="author">{% if talk.event_url %}<a href="{{ talk.event_url }}">{{ talk.event }}</a>{% else %}{{ talk.event }}{% endif %}</div>
        <div class="periodical"><em>{{ talk.venue }}</em>, {{ talk.date }}</div>
        <div class="links">
          {% if talk.video %}<a href="{{ talk.video }}" class="btn btn-sm z-depth-0" role="button">Video</a>{% endif %}
          {% if talk.slides %}<a href="{{ talk.slides | relative_url }}" class="btn btn-sm z-depth-0" role="button">Slides</a>{% endif %}
        </div>
      </div>
    </div>
  </li>
{% endfor %}
</ol>
</div>
