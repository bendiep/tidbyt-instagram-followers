load("render.star", "render")
load("http.star", "http")
load("xpath.star", "xpath")
load("encoding/base64.star", "base64")

INSTAGRAM_USER = "kimkardashian"
INSTAGRAM_PROFILE_URL = "http://localhost:8000/instagram/profile?user=" + INSTAGRAM_USER

INSTAGRAM_ICON = base64.decode("""
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
""")

def main():
    req = http.get(INSTAGRAM_PROFILE_URL)
    if req.status_code != 200:
        fail("Instagram request failed with status %d", req.status_code)

    print(req.json())
    follower_count = req.json()["follower_count"]

    return render.Root(
        child = render.Box( # This Box exists to provide vertical centering
            render.Row(
                expanded=True, # Use as much horizontal space as possible
                main_align="space_evenly", # Controls horizontal alignment
                cross_align="center", # Controls vertical alignment
                children = [
                    render.Image(src=INSTAGRAM_ICON),
                    render.Text(follower_count),
                ],
            ),
        ),
    )
