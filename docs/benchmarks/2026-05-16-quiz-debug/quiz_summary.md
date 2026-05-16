# Quiz Reasoning Benchmark

Generated: 2026-05-16 | mode: debug | debug=True

| model | quiz | cat | diff | ms | pass | partial | answer head |
|---|---|---|---|---|---|---|---|
| `llama3.2` | arith-01 | arithmetic | easy | 28902 | ❌ | 0.0 | Salience: Ah, a math problem on a manual... Not something I encounter often.

Cu |
| `llama3.2` | arith-02 | arithmetic | medium | 10107 | ❌ | 0.0 | "Wait, what's going on here? A baker with 3 dozen muffins... that's a lot of bak |
| `llama3.2` | logic-01 | logic | easy | 12378 | ✅ | 1.0 | The puzzle presents an intriguing challenge: "All birds can fly. Penguins are bi |
| `llama3.2` | logic-02 | logic | medium | 21622 | ✅ | 0.5 | Salience: Ah, the manual in front of me has some information that seems relevant |
| `llama3.2` | knowledge-01 | knowledge | easy | 10632 | ❌ | 0.0 | Another manual in front of me... I wonder what kind of information it might hold |
| `llama3.2` | knowledge-02 | knowledge | medium | 12302 | ✅ | 1.0 | The manual's question seems quite straightforward - "Which gas do plants release |
| `llama3.2` | reason-01 | reasoning | easy | 10066 | ✅ | 1.0 | "Wait, what's going on here? We've got Tom older than Bob, and Bob older than Al |
| `llama3.2` | reason-02 | reasoning | medium | 15218 | ❌ | 0.0 | The clock face is staring at me, and I'm drawn to the 3:15 mark. The hour hand i |
| `llama3.2` | creative-01 | creativity | easy | 15601 | ✅ | 1.0 | A robot with a love for rain... This feels novel and intriguing, but I'm not sur |
| `llama3.2` | creative-02 | creativity | medium | 10005 | ✅ | 1.0 | The eerie silence of an empty library is already unsettling enough, but the whis |
| `qwen2.5:7b` | arith-01 | arithmetic | easy | 42494 | ❌ | 0.0 | This simple arithmetic problem stands out due to its unexpected appearance in my |
| `qwen2.5:7b` | arith-02 | arithmetic | medium | 19724 | ❌ | 0.0 | This problem seems straightforward but requires careful attention to detail—some |
| `qwen2.5:7b` | logic-01 | logic | easy | 17836 | ✅ | 1.0 | This puzzle presents a clear contradiction to my existing knowledge of penguins. |
| `qwen2.5:7b` | logic-02 | logic | medium | 23982 | ✅ | 0.5 | The statement fits the pattern of modus ponens in reverse, which aligns with the |
| `qwen2.5:7b` | knowledge-01 | knowledge | easy | 17646 | ❌ | 0.0 | This question about the capital of France seems straightforward but taps into a |
| `qwen2.5:7b` | knowledge-02 | knowledge | medium | 17268 | ✅ | 1.0 | This question seems straightforward but hits on a fundamental process in biology |
| `qwen2.5:7b` | reason-01 | reasoning | easy | 18045 | ✅ | 1.0 | This problem presents a clear hierarchical relationship in ages, which aligns wi |
| `qwen2.5:7b` | reason-02 | reasoning | medium | 23299 | ❌ | 0.0 | The angle between the hour and minute hands at 3:15 presents an interesting geom |
| `qwen2.5:7b` | creative-01 | creativity | easy | 15427 | ✅ | 1.0 | The idea of a robot loving rain is intriguing; it challenges the typical percept |
| `qwen2.5:7b` | creative-02 | creativity | medium | 20566 | ✅ | 1.0 | The silence of the empty library, punctuated by the soft whispers of books, feel |

## Per-model summary

| model | total | passed | partial avg | wall sum (s) |
|---|---|---|---|---|
| `llama3.2` | 10 | 6 | 0.55 | 146.8 |
| `qwen2.5:7b` | 10 | 6 | 0.55 | 216.3 |