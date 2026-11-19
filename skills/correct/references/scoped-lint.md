# Turn a recurring correction into a scoped lint rule

Suppose agents keep delaying menu close with `setTimeout` because two components hold separate copies of the menu's open state. Give that state one owner first. If direct timers are still a recurring workaround in menu code, use the project's linter to guide callers to the supported state transition.

For a JavaScript project that already uses ESLint flat config, add an override to the existing config. This example assumes menu modules live under `src/ui/menu/` and the supported transition is `closeMenu()`. Use the project's real paths and API.

```js
{
  files: ["src/ui/menu/**/*.js"],
  languageOptions: {
    globals: { window: "readonly" },
  },
  rules: {
    "no-restricted-globals": [
      "error",
      {
        globals: [{
          name: "setTimeout",
          message: "Use closeMenu() from menu-state.js to update the shared menu state.",
        }],
        checkGlobalObject: true,
      },
    ],
  },
}
```

The rule covers direct calls and property access through recognized global objects such as `window.setTimeout`. If your config already declares browser globals, reuse that declaration. Unrelated modules keep their existing lint scope. [ESLint rule reference](https://eslint.org/docs/latest/rules/no-restricted-globals)

Prove the change with the project's normal lint command. Run it on a scratch copy containing the old timer and check that the diagnostic points to `closeMenu()`. Then restore the corrected call and check that lint passes. Include a legitimate timer outside the restricted paths in that pass. Run the close interaction separately to verify the menu actually closes without the flash. Keep any regression test with the journey it verifies.
