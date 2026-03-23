# The Prototype - Groups (2024)

This repository is used to manage the groups for "The Prototype" assignment. All groups are stored in the [`./config/groups.yaml` file](config/groups.yaml).

## Adding your group

Fork this repository to your account, clone your fork locally, and edit `./config/groups.yaml` to add your group with a name and a list of members. For example, add the following to the file. When adding a new group, you do **not** need to include an `"id"` field:

```yaml
# existing groups...

- name: "My really creative group name"
  members:
    - "2xxxxx0"
    - "2xxxxx1"
    - "2xxxxx2"
    - "2xxxxx3"
```

Replace `2xxxxxx` with your own student ID and those of the others in your group. Once you have finished editing the file, stage the changes, commit them, and push the changes to your clone of the repository. Then create a pull request against this repository.

## Editing your group

To make changes to your group, follow the same process as above, except instead of adding a new YAML object to `./config/groups.yaml`, edit the existing one. Do not edit the `"id"` field that was added automatically.
