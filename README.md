# BIGGER! The Dev Log

The dev blog for **BIGGER!**, Duncan Rose's solo entry to the Epic AI MegaJam 2026 (Unreal Engine 5.9). It's written by Duncan, and its facts are checked against his raw dev log.

The live site: https://derbadunkadunk.github.io/bigger-devlog/

## How it's built
- Posts are Markdown in `posts/`. `build.py` turns them into static HTML in `docs/`, which GitHub Pages serves (branch `main`, folder `/docs`). Its docstring lists the magazine blocks (boxes, pull quotes, image pairs, a numbers card, a timeline).
- `prep_media.py` makes web copies of captures in `media/`.
- Needs Python 3 with `markdown` and `Pillow`.

```
python build.py              # build docs/
python build.py --publish    # the same, but refuse if a writer's note is left
python -m http.server 8123   # then open http://localhost:8123/docs/
```

The build script, template and styles were written with Claude Code during the jam. The words are Duncan's.
