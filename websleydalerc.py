from websleydale import Site, build, directory, file, markdown, redirects, root, sass


def page(path, *args, header=None, title=None, toc=None, **kwargs):
    if header is not None:
        print(f"warning: page {path} has header={header!r}")
    if title is not None:
        print(f"warning: page {path} has title={title!r}")
    if toc is not None:
        print(f"warning: page {path} has toc={toc!r}")
    return markdown(path, *args, template="lumeh.html", **kwargs)


site = Site(
    name="lumeh.org",
    repo="https://github.com/kalgynirae/lumeh.org/",
    tree={
        "": page(root / "md/index.md"),
        "boxer/": page(root / "md/boxer.md"),
        "cafe/": page(root / "md/cafe/index.md"),
        "colin/": page(root / "md/colin/index.md"),
        "css/lumeh.css": sass(root / "css/lumeh.sass"),
        "css/normalize.css": file(root / "css/normalize.css"),
        "docs": directory(root / "docs"),
        "error/404.html": page(root / "md/error/404.md"),
        "font": directory(root / "font"),
        "guess": directory(root / "guess"),
        "image": directory(root / "image"),
        "jabberwockus/": page(root / "md/jabberwockus.md"),
        "js": directory(root / "js"),
        "lumeh/": page(root / "md/lumeh.md"),
        "media": directory(root / "media"),
        "music/": page(root / "md/music.md"),
        "poetry-yay/": page(root / "md/poetry-yay.md"),
        **{
            f"{path.relative_to(root/'projects').parent}/": page(path)
            for path in root.glob("projects/*/README.md")
        },
        "projects/pchyme/": page(root / "projects/pchyme/README.md", title="pchyme"),
        "projects/rockuefort/": page(
            root / "projects/rockuefort/README.md", title="rockuefort"
        ),
        "projects/slideception/": page(
            root / "projects/slideception/README.md", title="routemaster", toc=True
        ),
        "projects/thinking-green/": page(
            root / "projects/thinking-green/README.md", title="think-green"
        ),
        "projects/voidpop/": page(
            root / "projects/voidpop/README.md", title="websleydale"
        ),
        "projects/websleydale/": page(
            root / "projects/websleydale/README.md", title="websleydale"
        ),
        **{
            f"recipes/{name}.html": page(root / f"projects/recipes/{name}.md")
            for name in [
                "almond_salad_dressing",
                "apple_cider",
                "apple_crisp",
                "asparagus_mushroom_soup",
                "banana_bread",
                "bettys_chili",
                "calico_beans",
                "chana_masala",
                "chana_masala_with_spice_kit",
                "chancakes",
                "chicken_curry",
                "chili",
                "christmas_anything",
                "cookies",
                "cottage_pie",
                "creme_brulee_cheesecake",
                "dal",
                "first_watch_seasoning",
                "green_bean_bundles",
                "mac_and_cheese",
                "popovers",
                "pumpkin_bread",
                "quiche",
                "sweet_potato_casserole",
                "thai_chicken_curry",
            ]
        },
        "redirects.conf": file(root / "redirects.conf"),
        "robots.txt": file(root / "robots.txt"),
        "tools/krypto/": page(root / "md/krypto.md", header="md/krypto.header"),
        "tools/stopwatch/": page(
            root / "md/tools/stopwatch.md", header="md/tools/stopwatch.header"
        ),
        "wiki/": page("md/wiki.md"),
        **{
            f"{path.relative_to(root/'md').with_suffix('')}/": page(path)
            for path in root.glob("md/wiki/**/*.md")
        },
    },
)
build(site, dest="out")
