---
title: Speed is a design decision
cat: TECHNICAL SEO
date: JUL 2026
iso: 2026-07-14
excerpt: Slow websites are rarely a hosting problem. They are usually decided in the design phase, by choices about images, fonts and effects. Here is how to make speed part of the design instead of a fix at the end.
---
When a site feels slow, the first instinct is to blame the hosting. Sometimes that is fair. But in most of the slow sites I audit, the server is fine. The weight comes from decisions made much earlier, while the site was being designed: a huge video in the header, five different fonts, a slider nobody asked for, and images exported straight from a camera.

That is why I think of speed as a design decision. It is far easier to design a fast site than to make a slow one fast afterwards.

## Why speed matters to a small business

Visitors are impatient, especially on phones and especially on mobile data. Every extra second of loading is another chance for them to give up and try a competitor.

Google cares too. It measures real visitors' experience with a set of scores called Core Web Vitals and uses them as one of many signals when ranking pages. In plain terms, they ask three questions:

- How quickly does the main content appear? Google's target is within 2.5 seconds.
- How quickly does the page react when someone taps or clicks? The target is 200 milliseconds or less.
- Does the layout stay still while it loads, or do things jump around? Jumping content is what makes people tap the wrong button.

Speed alone will not rank a thin page above a genuinely useful one. But when two pages are similarly helpful, the faster one has the edge, and it converts better either way.

## The design choices that decide your speed

Most of the weight on a typical small business site comes from a handful of places. Each one is a choice.

Images. A single photo from a modern phone can be several megabytes. Shown at the size of a card on a website, it needs a fraction of that. Resizing images to the size they are displayed at, and saving them in modern formats like WebP or AVIF, often cuts page weight in half on its own.

Video backgrounds. They look impressive in a design review and cost a lot on a phone. If the video does not explain something, a strong still image usually does the job better.

Fonts. Every font family, and every weight of it, is another file to download. Two families with a couple of weights each is plenty for most sites.

Sliders and carousels. They add scripts, they hide most of their content, and research on how people use them has not been kind for years. A single clear message beats five rotating ones.

Third-party extras. Chat widgets, several tracking tools, social feeds and pop-up tools each load their own code. Individually small, together they can double the time before a page responds.

## Designing fast from the start

On my own projects, I set a simple budget before any visuals are made: roughly how heavy the homepage is allowed to be, and how many fonts and scripts it can use. Then design happens inside that budget, the same way it happens inside a brand's colours.

A few habits help:

- Design the mobile version first. It forces you to decide what actually matters.
- Reserve space for images and embeds, so the layout does not jump when they arrive.
- Load what is visible first. Images further down the page can wait until the visitor scrolls near them.
- Question every effect. If an animation does not help someone understand or act, it is decoration, and decoration has a cost.

## How to check your own site

You do not need to be technical to get a useful read. Open PageSpeed Insights, paste in your homepage and look at the mobile results. The top section shows how real visitors experienced your site over the last month, if Google has enough data. The lower section is a lab test with a list of suggestions.

Do not obsess over reaching a perfect 100. Focus on whether the three Core Web Vitals are marked as good, and on the biggest items in the suggestions list, which are usually images.

If the report is a wall of red and you are not sure where to start, send me the link. In most cases the fix is a short list, and it starts with the design choices above rather than a new server.
