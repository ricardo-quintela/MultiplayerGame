By [Tiago Tamagusko](https://gist.github.com/tamagusko/fbdb7e87358006cdaab9a7c67eacb511)

# Semantic Commit Messages

See how a minor change to your commit message style can make you a better programmer.

Format: `<type>(<scope>): <subject>`

`<scope>` is optional

## Example

```
feat: add hat wobble
^--^  ^------------^
|     |
|     +-> Summary of the change.
|
+-------> Type: build, docs, feat, fix, perf, refactor, or test.
```

More Examples:

- `build`: Changes that affect the build system or external dependencies (example scopes: gulp, broccoli, npm)
- `docs`: Documentation only changes
- `feat`: A new feature
- `fix`: A bug fix
- `perf`: A code change that improves performance
- `refactor`: A code change that neither fixes a bug nor adds a feature
- `test`: Adding missing tests or correcting existing tests
- `wip`: Work in progress
