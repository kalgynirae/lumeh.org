from websleydale import Site, build, directory, file, markdown, root, sass


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
    tree={
        "css/lumeh.css": sass(root / "css/lumeh.sass"),
        "css/normalize.css": file(root / "css/normalize.css"),
        "docs": directory(root / "docs"),
        "font": directory(root / "font"),
        "guess": directory(root / "guess"),
        "image": directory(root / "image"),
        "js": directory(root / "js"),
        "media": directory(root / "media"),
        "favicon.ico": file(root / "image/favicon.ico"),
        "robots.txt": file(root / "robots.txt"),
        "boxer.html": page(root / "md/boxer.md"),
        "index.html": page(root / "md/index.md"),
        "jabberwockus.html": page(root / "md/jabberwockus.md"),
        "krypto.html": page(root / "md/krypto.md", header="md/krypto.header"),
        "lumeh.html": page(root / "md/lumeh.md"),
        "music.html": page(root / "md/music.md"),
        "poetry-yay.html": page(root / "md/poetry-yay.md"),
        "unofficial_opposites.html": page(root / "md/unofficial_opposites.md"),
        "blog/index.html": page(root / "md/blog/index.md"),
        "cafe/index.html": page(root / "md/cafe/index.md"),
        "colin/index.html": page(root / "md/colin/index.md"),
        "error/404.html": page(root / "md/error/404.md"),
        "tools/stopwatch.html": page(root / "md/tools/stopwatch.md"),
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
        "projects/pchyme/index.html": page(root / "projects/pchyme/README.md", title="pchyme"),
        "projects/rockuefort/index.html": page(
            root / "projects/rockuefort/README.md", title="rockuefort"
        ),
        "projects/slideception/index.html": page(
            root / "projects/slideception/README.md", title="routemaster", toc=True
        ),
        "projects/thinking-green/index.html": page(
            root / "projects/thinking-green/README.md", title="think-green"
        ),
        "projects/voidpop/index.html": page(
            root / "projects/voidpop/README.md", title="websleydale"
        ),
        "projects/websleydale/index.html": page(
            root / "projects/websleydale/README.md", title="websleydale"
        ),
        "tools/stopwatch.html": page(
            root / "md/tools/stopwatch.md", header="md/tools/stopwatch.header"
        ),
    },
)
build(site, dest="out")

redirects = {
    "/games/narchanso.html": "/wiki/narchanso-ball.html",
    "/recipes/mung_bean_dahl.html": "/recipes/mung_bean_dal.html",
}
