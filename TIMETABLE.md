# Updating the class timetable

The website timetable is built from one small file: `schedule.js`.
The social media poster and the website stay in sync if both come from the same prompt.

## Workflow

1. Ask ChatGPT (or any AI agent) for the new poster, and in the same conversation paste the prompt below.
2. Replace `schedule.js` in this folder with the file it gives you.
3. Replace `assets/timetable.webp` with the new poster (keep the file name).
4. Commit and push:

   ```
   git add schedule.js assets/timetable.webp
   git commit -m "Update class timetable"
   git push
   ```

The site shows the new timetable within a minute or two. Nothing else in the page needs to change.

## Prompt to paste into ChatGPT

> Now give me the same timetable as a file called `schedule.js`, in exactly this format.
> Keep the class keys that already exist (hyrox, gap, trx, mobility, abs, bike, pilates, hiit).
> If there is a new class, add a new key with a short English description (`en`) and the Portuguese name (`pt`).
> Use 24h times like "09:30", days as mon, tue, wed, thu, fri, sat, sun, and set `isNew: true` for classes marked as new.
> Set `updated` to today's date. Output only the file contents.
>
> (then paste the current contents of schedule.js)

## Quick checks before pushing

- Every `class` value in `sessions` must exist in `classes`, otherwise the site shows the raw key.
- Open `index.html` locally (or `python3 -m http.server 8000`) and look at the Classes section.
