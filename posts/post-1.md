---
title: A day ahead of schedule
slug: post-1
order: 1
kicker: Post 1 · Night 0 + Thursday
dateline: Nov 11–13, 2026
standfirst: Night 0 and the first full day: a falling-sand sim pulled into 3D, three looks thrown out, a car made of sand, and a water tower that refused to fall over.
hero: D3-1401-scene2-flood-and-fire.jpg
hero_alt: A voxel western street: water floods the ground under a raised iron tank, and a wooden saloon is on fire.
hero_caption: Scene 2, the Saloon Flood, in an early scripted take: water pours from the tank and floods the street while the saloon burns. Thu 2:01 PM.
---

Welcome to BIGGER!, where your job is to come up with the most spectacular SFX you can for each of the movie's unique scenes. Once the job is done, you are treated to the final film with your best shots. Just remember: the Director always wants you to go BIGGER!

## Night 0: sand on screen

When I first heard the theme for this game jam was 'Director's Cut', I was very excited, because I knew I would be able to utilize the theme in two different ways. The first was the one feature that I've always had to (Director's) cut: falling-sand fluid physics and interactions, but in a unique way or direction. The second was integrating it into a movie- and set-based game. The idea was to combine the two into a game where you interact with the falling-sand systems to create your own special effects for different scenes.

As you can see in the images below, I went through some iterations until I had a halfway satisfactory fluid system. I noticed water falling in even bars; Claude found that every grain sped up the same way, and a coin flip fixed it. Claude was excellent for this use case, as it created the sim for me in C++ in a timeframe I would never have managed. Once I was at this point, I knew I had to make it unique and interesting, and differentiate it from other falling-sand games.

::: pair
![Water falling off a ramp in evenly spaced horizontal bars.](media/D1-0010-water-banding-before.jpg "12:10 AM: water off the ramp falls in even bars.")
![The same pour falling as an irregular stream.](media/D1-0012-water-banding-after.jpg "12:12 AM: each grain speeds up on a coin flip, and the bars break into a stream.")
:::

## Three looks, all wrong

Two hours into the jam, I had Claude put three looks side by side on one sheet: a miniature diorama, a glossy blockbuster and a clean toon, all running the same frozen frame of the same sim. They were all decent enough, but I immediately knew none of them was what I was going for, or interesting enough. Another issue was that I wasn't sure how to make SFX creation work from a 2D side view. With both of these concerns in mind, it was clear I had to rethink the look.

![A sheet comparing four looks of the same falling-sand frame.](media/D1-0105-style-spike-sheet.jpg "1:05 AM: one frozen frame, three looks plus a control. I turned all three down.")

At this point, Claude laid out three ways to bring the sand into 3D and recommended voxels, which is where I'd assumed we'd go. I agreed, with one condition:

::: pull | Me, Thu 1:15–2:00 AM
Voxel destruction based games are extremely common and the last thing I want is for this to look or play like other games.
:::

I asked Claude for a look sheet of some possibilities and received not-bad results. It drew the 3D sand as clay, tiny grains and smooth toys, but the voxels looked strange (ugly) and also too familiar (cookie-cutter voxel). I started to panic. I wasn't sure I was going to be able to accomplish the look, or, more importantly, the gameplay I had dreamed up, and I was worried I was going to have to start totally fresh and come up with a new plan.

So I suggested 2D particles in a 3D world. Claude mocked up two versions, and one was a true marriage between the two: a 3D sim drawn as pixel tiles. This look fit almost exactly what I had in my head, while letting us play with falling sand and explosives in 3D.

::: pair
![One 3D sand frame drawn three ways: clay, tiny grains and smooth toy surfaces.](media/D1-0135-3d-look-spike-sheet.jpg "1:35 AM: round two, the same 3D frame as clay, tiny grains and smooth toys. It looked strange.")
![A sheet comparing two 3D looks of the same take.](media/D1-0155-pixels-in-3d-AB-sheet.jpg "1:55 AM: round three. A, the 3D sim drawn as pixel tiles, became the look.")
:::

## How I work: one conversation per pass

I have three custom Claude skills that I made and utilize throughout this project. They are very simple, but they let me build out each feature or step I have planned methodically and completely.

![A sidebar group named BIGGER! jam, listing eight conversations from the jam setup up to this dev blog.](media/sidebar-bigger-jam.png "My sidebar: one conversation per pass, oldest at the bottom. The top one is this blog."){: .side}

The first is my /pass skill, which breaks what we need to complete into sensible, orderly 'passes'. Each pass gets its own fresh Claude conversation, at the very least, and usually begins with questions (with recommendations), look-first sheets (if the work is visual), then the build, tests that prove they can fail, and a commit.

The second is my /handoff skill, which I use at the end of each pass, or when the context in a session is getting too large. It makes sure the work in that conversation is buttoned up and documented, creates a handoff document for the next conversation to read (essentially everything needed for that pass), and finally gives me the prompt to start that new conversation with. This workflow also makes it very easy to know where you are in the project, and which conversation holds which piece of the work.

The third is my dev-knowledge plugin (multiple skills), which contains the tips and preferences I've learned from using different engines and tools, such as Unreal, Meshy, packaging, etc.

::: timeline | Seven conversations so far
Wed 11:05 PM | Setup and jam start | Project created, Unreal MCP checked, first Diversion commit at 11:31 PM.
Wed 11:46 PM | Night 0: the falling-sand grid | Ten questions. First pour by hand at 12:19 AM.
Thu 12:35 AM | Day 1: reactions and style spike | Fire, the move into 3D, the first deterministic blast.
Thu 2:40 AM | Day 2: game loop | Take record, first package, the first full take.
Thu 4:13 AM | Scene 1 and packaging | The Rodin car, three play tests, liquids that read.
Thu 9:10 AM | Scenes 2 and 3 | Floods, falling solids, the reel, stress and tipping, rigging shots.
Thu 10:34 PM | The juice pass | Shake, flashes, Niagara, fire lights, the Prep drift.
:::

::: box | The toolkit
- **`pass`** (my skill, written before the jam): questions with recommendations first, a model plan, look-first sheets before anything visual, rule bends named before they're made, every test re-run, and a ledger of which model did what.
- **`handoff`** (mine, pre-jam): closes a conversation, commits, writes the next pass's brief and gives me the opening prompt for a fresh conversation.
- **`dev-knowledge`** (mine, pre-jam): my own notes on Unreal, packaging and AI-mesh cleanup, read before touching those tools.
- **Unreal MCP** (built into UE 5.9): Claude drives the editor directly. **Diversion** for the game's version control, **Hyper3D Rodin** for models, **Blender** run headless from scripts, **ElevenLabs** for the director's voice.
:::

::: box | How I work with AI
- **I decide:** the idea, every look (picked from sheets), the scenes, every play test and what it should feel like.
- **Claude (Opus 5.5)** writes the C++ and the scripts, drives the editor, shoots the sheets and clips, runs the tests and packages the game.
- **A second model (Fable 5.2)** reviews most of the big designs before they're built.
- **A Sonnet 5.5 subagent** did one cleanup job: removing the old 2D code, with every line of its change read before it went in.
- **Claude never posts or submits for me.**
:::

## What's done

Currently, each scene starts with the brief, outlining the scene and the goals to achieve. You then have access to different fluids and explosives to try to create the best SFX you can. When you're ready, the Director yells 'Action!' and you get to see whether your stuntman makes it through in one piece. When you have completed all the scenes, a 'Director's Cut' is re-simulated from each take's record, showing you your best takes. I also have the basic look and models outlined, created and implemented. Time permitting, I plan to go over everything with a fine-tooth comb, as I haven't yet spent the time I'd like to on each asset.

![A CUT card over a voxel car: "CUT! That's it? I said BIGGER!" with zero stars.](media/D2-0321-first-cut-card.jpg "3:21 AM: the first full take, played by a script. 0 stars, 9% of the car destroyed.")

::: pair
![A red 1970s sedan model on a grey background.](media/D2-0416-rodin-car-threequarter.jpg "4:16 AM: the car from Rodin, one text prompt, cleaned in Blender and checked for logos.")
![A sheet of four voxel cars in a street set.](media/D2-0430-car-look-sheet.jpg "4:30 AM: the car as cells, four ways. I picked the hollow shell: it opens up when it blows.")
:::

::: wide
![Scene 2: a water tank on iron legs tips through a saloon wall and bursts.](media/D3-1929-scene2-iron-legs-tank-into-saloon.mp4 "7:29 PM: the tank tips through the saloon wall and bursts. A silent editor recording.")
:::

::: numbers | By the numbers, Fri 1:45 AM
70 | git commits since the jam began
52 | Diversion commits (the game)
49 | automated tests
10 | packaged Windows builds
3 | scenes
12 | sim materials
14 | Rodin models
7 | Claude Code conversations
101 | captures in the raw log
:::

## What broke

The tools to create and place your sand and explosives were not at all intuitive or easy to use at first. It has taken constant change and iteration to keep the controls and tools intuitive while making them as dynamic and useful as possible, and I imagine I will continue to iterate on this non-stop until submission. For instance, the Powder Line (fuse) tool was too loose to place and broke its connections regularly (without you being able to tell), leading to an extremely underwhelming scene where only the first chunk of a fuse would burn. I fixed this by making the powder easier to place, and it now shows an orange line through and up to where the fuse will burn. Now it's easy to tell whether your connections are broken.

![A powder line glowing all the way to its charge, and below it a broken line whose glow stops short.](media/D3-1604-fuse-glow-whole-vs-broken.jpg "4:04 PM: the fuse check in Prep. Top, the whole line glows to the charge; bottom, the line is broken and the glow stops short.")

Beyond that, another issue I had was the water tank in Scene 2. With the ability to destroy a raised water tank, you would hope its structure would fracture under stress, fall and break in a satisfying way. This took many attempts to get to a tank that falls the way you’d expect. I blew three of its four legs, and it still stood on the last one. Claude traced it in the code: the tank was holding itself up with its own water. So I asked, “are we able to make it so materials have a stress limit so it would tip over and be destroyed how you expect?” Claude wrote a design for load, tipping and breaks, Fable 5.2 reviewed it before any of it was built, and two spikes later the gag worked: blow the two legs on the saloon side, and the tank tips through the saloon wall, bursts and floods the street. This seems like a perfect use case for Claude, and thanks to how quickly it can iterate and figure out the code or calculations we need, I am able to work until we get the exact destruction I want.

![A water tank standing on one remaining leg.](media/D3-1524-scene2-tank-on-one-leg.jpg "3:24 PM: three legs blown, and the tank still stood on the fourth, held up by its own water.")

## What worries me

I'm having a hard time judging the difficulty of the scenes, and what order they should go in. It's difficult to drill down into the details and make each one challenging without it being a frustrating experience.

## Next

I have the basic gameplay and look of my game. Now I want to make it as fun as possible while ensuring the gameplay is almost self-explanatory. I also want to continue to iterate on, improve and add to whatever models or structures the game has, making it look fully fledged and professional.
