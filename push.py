from huggingface_hub import create_repo, upload_folder, whoami


def main(
    huggingface_repo: str,
    github_repo: str,
    token: str,
    repo_type: str = "space",
    space_sdk: str = "gradio",
    private: bool = False,
):
    print("Syncing with Hugging Face Spaces...")

    if huggingface_repo == "xx":
        huggingface_repo = github_repo

    if "/" not in huggingface_repo:
        # Case namespace is implicit
        username = whoami(token=token)["name"]
        huggingface_repo = f"{username}/{huggingface_repo}"
    print(f"\t- Repo ID: {huggingface_repo}")

    print(f"\t- Github_repo: {github_repo}")
    url = create_repo(
        huggingface_repo,
        token=token,
        exist_ok=True,
        repo_type=repo_type,
        space_sdk=space_sdk if repo_type == "space" else None,
        private=private,
    )
    print(f"\t- Repo URL: {url}")

    latter_repo = github_repo.split("/")[1]
    directory = f"work/{latter_repo}/{latter_repo}"

    # Sync folder
    commit_url = upload_folder(
        folder_path=directory,
        repo_id=huggingface_repo,
        repo_type=repo_type,
        token=token,
        commit_message="Synced repo using 'sync_with_huggingface' Github Action",
        ignore_patterns=["*.git*", "*README.md*"],
    )
    print(f"\t- Repo synced: {commit_url}")


if __name__ == "__main__":
    from fire import Fire

    Fire(main)