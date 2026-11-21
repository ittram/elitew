/*
  ELITE WELLNESS: the Instagram posts shown before the footer (version 3.3 of the site, ?ig=posts).
  The page builds a strip of tall cards from this file. Two ways to fill it:

  1. By itself. Connect the gym's Instagram to a feed service (for example behold.so, free for one
     account), and paste the feed address it gives into `feed`. The newest posts then show on their own.
     e.g. feed: 'https://feeds.behold.so/AbC123xyz'

  2. By hand. Save each post's picture in assets/instagram/ and list it in `posts`, newest first:
     { url:'https://www.instagram.com/p/DAbCdEfGhIj/', img:'assets/instagram/2026-11-18-hyrox.webp',
       alt:'Saturday HYROX class on the turf', altPt:'Aula de HYROX de sábado na relva', video:false }
     Pictures are 4:5 upright (1080 x 1350 is what Instagram uses), in colour.

  While both are empty the strip shows numbered placeholders, so the layout can be judged.
*/
window.EW_INSTAGRAM = {
  profile: 'https://www.instagram.com/elitewellnessbysantos/',
  feed: '',
  posts: []
};
