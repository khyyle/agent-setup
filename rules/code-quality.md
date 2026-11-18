# Writing code a reader can follow

## Name the distinction

Choose names a reader can use to predict a decision. A solver may finish without converging. Its loop can test `finished` while the caller tests `converged` to decide whether to try a fallback. A single `done` flag would hide the distinction. In a language with sum types, a result with cases such as `Converged` and `IterationLimit` can express it directly. In a numerical kernel, flags may fit the representation better.

Name policies and thresholds where they are set. Carry units across boundaries when a bare value is ambiguous, as in `timeout_ms` or `noise_variance`. A local `i` is fine for a short loop, and `k` is useful for a frequency index next to its defining equation. Names like `handle_data` give callers little basis for understanding effects. `decode_record` and `append_record` describe different promises.

## Put the explanation where the reader needs it

- **Module or file introduction.** Say what question the module answers or which boundary it owns. State a convention that affects interpretation, such as whether coordinates are pixel centers or edges. For a scientific result, give its meaning and the assumptions behind it. Link a longer derivation if useful and keep the assumption needed to use the code in the module.
- **Section or block.** Give the reader the intermediate result to expect, the invariant a phase establishes, or the reason two steps must occur in this order. A short worked example can explain an indexing algorithm better than a page of prose. Name a section for its job. A heading like “Setup” gives little help on its own.
- **Beside an operation.** Put a brief note immediately beside an expression when the reader needs a unit, boundary convention or mathematical identity to understand it. Move a longer explanation above the operation so both code and prose are easy to scan.
- **What to leave out.** Skip line-by-line narration, commented-out code, change history, and inventories of current callers. Refer to a symbol or source when it explains a real contract. Keep the comment accurate when the contract changes.

In a numerical routine, an array shape error can survive every check of the output dimensions. This comment explains the failure a future edit could introduce when `residuals` has shape `(sensors, samples)`.

```python
# Each sensor has its own noise estimate. The singleton axis applies that
# estimate to every sample from the sensor. If the array happens to be square,
# a bare vector would silently weight the samples along the wrong axis.
standardized_residuals = residuals / noise_std_by_sensor[:, None]
```

In a block reader, the caller needs the interval convention. The person changing the arithmetic also needs to know why it subtracts one.

```cpp
#include <cstddef>
#include <stdexcept>

// Count storage blocks intersecting the half-open byte range [begin, end).
std::size_t blocks_touched(std::size_t begin, std::size_t end, std::size_t block_bytes) {
    if (block_bytes == 0 || end < begin) {
        throw std::invalid_argument("Expected a positive block size and an ordered byte range");
    }
    if (begin == end) return 0;

    const auto first_block = begin / block_bytes;
    const auto last_block = (end - 1) / block_bytes;  // An aligned end would otherwise count the next block.
    return last_block - first_block + 1;
}
```

## Decide where a helper belongs

Read the caller after the proposed extraction. Can a reader still see which input selects a branch, when state changes, and what happens on failure?

- **Keep steps inline** when order is the point. In an import, parsing a batch, checking it, then publishing the result tells the reader when the new data becomes visible. Hiding the check and the write together behind `finish_batch` obscures what a failed check protects.
- **Use a private helper** when the operation has a meaningful input and result, even with a single caller. A helper that decodes one record can own the wire format. Keep its inputs and dependencies explicit and choose the narrowest scope that fits the language.
- **Share across modules** when callers depend on the same contract. A file reader and an index builder that both interpret the same on-disk block format should agree on which blocks a byte range touches. Give that calculation to the format owner. Similar arithmetic on screen coordinates can stay with the renderer if its endpoint convention differs.

Line count can prompt a second look. The extraction earns its place when it makes the remaining code easier to understand or gives an invariant a clear owner.
