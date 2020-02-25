from websleydale import Author, Site, build, directory, file, markdown, root, sass


def page(path, *args, header=None, title=None, toc=None, **kwargs):
    if header is not None:
        print(f"warning: page {path} has header={header!r}")
    if title is not None:
        print(f"warning: page {path} has title={title!r}")
    if toc is not None:
        print(f"warning: page {path} has toc={toc!r}")
    return markdown(path, *args, template="lumeh.html", **kwargs)


site = Site(
    known_authors={
        Author(
            display_name="kalgynirae",
            email="colinchan@lumeh.org",
            url="https://github.com/kalgynirae/",
        )
    },
    name="lumeh.org",
    repo_name="kalgynirae/lumeh.org",
    repo_url="https://github.com/kalgynirae/lumeh.org",
    tree={
        "/css/lumeh.css": sass(root / "css/lumeh.sass"),
        "/css/normalize.css": file(root / "css/normalize.css"),
        "/docs": directory(root / "docs"),
        "/font": directory(root / "font"),
        "/guess": directory(root / "guess"),
        "/image": directory(root / "image"),
        "/js": directory(root / "js"),
        "/media": directory(root / "media"),
        **{
            f"/{path.relative_to(root).parent}/": page(path)
            for path in root.glob("projects/*/README.md")
        },
        **{
            f"/recipes/{name.replace('_', '-')}/": page(
                root / f"projects/recipes/{name}.md"
            )
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
        "/redirects.conf": file(root / "redirects.conf"),
        "/robots.txt": file(root / "robots.txt"),
        **{
            f"/{path.relative_to(root/'pages').with_suffix('')}/": page(path)
            for path in root.glob("pages/**/*.md")
        },
        "/": page(root / "pages/index.md"),
    },
)
build(site, dest="out")
