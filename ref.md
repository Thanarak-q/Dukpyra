## TL;DR

Source-to-source research splits into rule-based AST rewriting, language-parametric ASTs, runtime type collection for dynamic-to-static translation, and neural unsupervised methods; successful systems combine declarative/transformation frameworks with profiling or user-guidance to handle typing and optimization.

----

## Techniques and methodologies

This section summarizes principal translation paradigms and how they are implemented in recent research. It outlines rule-driven AST rewriting, declarative transpilation, neural models, and hybrid approaches used in practice.

- **Rule driven AST rewriting** Traditional transcompilers rely on handcrafted rewrite rules applied to source ASTs; this is the baseline that newer systems compare against, as discussed in "Unsupervised Translation of Programming Languages" by Marie-Anne Lachaux et al. [1].  
- **Declarative one-to-many transpilation** The Basilisk architecture instantiates a declarative transpilation infrastructure called Hydra to generate multiple target languages from a single kernel, enabling systematic one-to-many source-to-source generation (Francesco Bertolotti et al.) [2].  
- **Language-parametric ASTs** Incremental parametric syntax represents programs so transformations generalize across languages; Cubix (James Koppel et al.) demonstrates building the same refactoring across C, Java, JavaScript, Lua, and Python by reusing parametric syntax components [3].  
- **Neural unsupervised transcompilation** Fully unsupervised neural models trained on monolingual code can translate functions between languages without parallel corpora; Lachaux et al. train such a model and report higher accuracy than rule-based commercial baselines, plus they release an 852-function parallel test set [1].  
- **User-guided incremental rule construction** DuoGlot (Bo Wang et al.) constructs translation rules incrementally, letting users provide localized guidance to resolve the “last mile” errors common in automatic translators and improving overall correctness on benchmarks [4].

----

## Compiler design patterns

This section ties architectural choices to maintainability, extensibility, and multi-language support, and cites concrete frameworks and their design rationales. It emphasizes reuse, modularity, and parametric representations.

- **Platform plus language abstraction** Basilisk separates a transpilation layer (Hydra) from a platform abstraction layer (Wyvern), enabling language- and platform-independent development; Hydra generates seven targets and was evaluated across heterogeneous hardware for portability (Francesco Bertolotti et al.) [2].  
- **Parametric transformation engines** Cubix implements incremental parametric syntax so once a transformation is written it requires little work to adapt to another language, preserving source structure and producing readable output (James Koppel et al.) [3].  
- **Templates and transformation synergy** Model-driven work emphasizes combining transformations with templates to maximize reuse of code generators and to systematically manage generator variability (Robert Eikermann et al.) [5].  
- **Incremental and customizable pipelines** DuoGlot embodies an incremental pipeline that builds and reuses localized rules, enabling user customization and higher translation accuracy on scripting-to-scripting tasks (Bo Wang et al.) [4].

----

## Dynamic to static

This section focuses on translating dynamic-language idioms to static-typed targets, concrete techniques for recovering types, and limitations observed in the literature. It concentrates on empirical strategies and their constraints.

- **Runtime type collection** One practical approach is to collect types at runtime and use them to annotate the generated static code; the method and trade-offs are described in "Runtime type collecting and transpilation to a static language" by P. Krivanek and R. Uttner, which uses runtime-collected types to enable transpilation into C# and documents limitations such as unsupported stateful traits [6].  
- **Using the source as high-level IR** Bysiek et al. treat Python as a high-level IR for JIT translation and apply performance-oriented transformations and directives to produce efficient static-like output, demonstrating that retaining high-level semantics eases certain translations from Python to optimized code (Mateusz Bysiek et al.) [7].  
- **Practical restrictions and user involvement** DuoGlot’s user-guidable rule construction is a response to dynamic features that resist full automation; localized user guidance is used to resolve parts of programs where automatic rules fail, improving real-world translation success (Bo Wang et al.) [4].  
- **Insufficient evidence** Specific systematic mappings for advanced dynamic features (for example, complete handling of duck typing, arbitrary metaprogramming, or stateful runtime traits across many language pairs) are not fully detailed across the supplied corpus, and so comprehensive general-purpose algorithms for all such features cannot be stated from these papers alone.

----

## Performance and optimization

This section reviews strategies to preserve or improve performance through IR choices, code transformations, directives, and evaluation results reported in studies. It highlights cross-language benchmarking practice.

- **High-level IR and JIT combined with transformations** The approach in "Towards Portable High Performance in Python" uses Python as a high-level IR, applies code transformations and compiler directives, and performs JIT compilation to achieve performance superior to prior acceleration methods, as evaluated by Mateusz Bysiek et al. [7].  
- **Cross-target performance evaluation** Basilisk/Hydra validated portability by transpiling algorithms from the Rodinia suite into seven languages and running 35 benchmarks on four hardware platforms, demonstrating the infrastructure’s ability to target performance across languages and hardware (Francesco Bertolotti et al.) [2].  
- **Benchmarking multilingual generation** MultiPL-E (the MultiPL-E system) shows how translating unit-test-driven benchmarks to many languages enables systematic evaluation of code generation quality across languages and models, informing performance and correctness trade-offs for transpilation and neural generation pipelines [8].  
- **Optimization levers used** The cited systems use a combination of: **profile-driven typing** (runtime type collection) [6], **transformation-driven optimizations and directives** (Bysiek et al.) [7], and **target-specific code patterns produced by declarative generators** (Hydra) [2].

----

## Case studies and future trends

This section collects representative implementations, their outcomes, and emerging directions the papers identify or exemplify. It concludes with likely research trajectories grounded in the supplied work.

- **Basilisk with Hydra and Wyvern** Francesco Bertolotti, Walter Cazzola, Dario Ostuni, and Carlo Castoldi present Basilisk and the Hydra transpiler to target D, C++, C#, Scala, Ruby, Hy, and Python, evaluating 35 benchmarks from Rodinia across four platforms to show language- and platform-independent deployment [2].  
- **Unsupervised neural transcompiler** Marie-Anne Lachaux, Baptiste Roziere, Lowik Chanussot, and Guillaume Lample build a fully unsupervised neural transcompiler that translates functions between C++, Java, and Python, outperforming rule-based commercial baselines and releasing an 852-function parallel test set for evaluation [1].  
- **DuoGlot user-customizable transpiler** Bo Wang, Aashish Kolluri, Ivica Nikolić, Teodora Baluţa, and Prateek Saxena implement DuoGlot for Python-to-JavaScript translation, achieving ~90% accuracy on GeeksForGeeks benchmarks by incrementally constructing and reusing translation rules with user guidance [4].  
- **Cubix language-parametric transformations** James Koppel, Varot Premtoon, and Armando Solar-Lezama demonstrate that incremental parametric syntax enables multi-language refactorings that preserve readability and structure, validated by human studies and compiler test suites [3].  
- **Emerging trends** The corpus points to several converging directions: **unsupervised neural translation and large-scale multilingual benchmarks** to reduce parallel-data dependence [1] [8], **language-parametric and reusable AST representations** to scale transformations across languages [3], **user-in-the-loop and incremental rule systems** to manage edge cases and increase correctness [4], and **integrating platform abstraction with transpilation** for end-to-end portability (Basilisk) [2].  
- **Insufficient evidence** While the papers illustrate many promising directions, comprehensive solutions that fully automate translation of all dynamic-language idioms to fully-typed static equivalents across arbitrary language pairs are not demonstrated within the provided corpus.


References
[1]
M.-A. Lachaux, B. Roziere, L. Chanussot, and G. Lample, “Unsupervised Translation of Programming Languages,” arXiv: Computation and Language, June 2020.
[2]
F. Bertolotti, W. Cazzola, D. Ostuni, and C. Castoldi, “When the dragons defeat the knight: Basilisk an architectural pattern for platform and language independent development,” Journal of Systems and Software, May 2024, doi: 10.1016/j.jss.2024.112088.
[3]
J. Koppel, V. Premtoon, and A. S. Lezama, “One tool, many languages: language-parametric transformation with incremental parametric syntax,” Oct. 2018.
[4]
“User-Customizable Transpilation of Scripting Languages,” Jan. 2023, doi: 10.48550/arxiv.2301.11220.
[5]
R. Eikermann, K. Hölldobler, A. Roth, and B. Rumpe, “Reuse and Customization for Code Generators: Synergy by Transformations and Templates,” pp. 34–55, Jan. 2018, doi: 10.1007/978-3-030-11030-7_3.
[6]
“Runtime type collecting and transpilation to a static language”, [Online]. Available: https://ceur-ws.org/Vol-3893/Paper08.pdf
[7]
M. Bysiek, M. Wahib, A. Drozd, and S. Matsuoka, “Towards Portable High Performance in Python: Transpilation, High-Level IR, Code Transformations and Compiler Directives,” no. 38, pp. 1–7, July 2018.
[8]
“MultiPL-E: A Scalable and Extensible Approach to Benchmarking Neural  Code Generation,” Aug. 2022, doi: 10.48550/arxiv.2208.08227.