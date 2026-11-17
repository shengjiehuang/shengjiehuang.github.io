---
layout: page
permalink: /teaching/
title: Teaching
description:
nav: true
nav_order: 5
---

<!--
  To add a course, create a file in the _teachings/ folder, for example _teachings/phy5000-fall-2026.md:

  ---
  layout: course
  title: PHY 5000 Quantum Mechanics
  description: One or two sentences about the course.
  instructor: Sheng-Jie Huang
  year: 2026
  term: Fall
  location: Room, building
  time: Days and time
  course_id: phy5000-fall-2026
  ---

  Course details, syllabus link, etc.

  Courses are listed on this page automatically, newest year first.
-->

{% if site.teachings.size > 0 %}
{% include courses.liquid %}
{% else %}
PHY6937/PHY4936, Introduction to Quantum Computing, Fall 2026
{% endif %}
