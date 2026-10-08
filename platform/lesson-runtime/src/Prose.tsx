// Copyright © 2026 Christopher Snow

// Markdown prose, rendered the same way everywhere: GitHub tables and lists, maths through
// KaTeX. The app imports KaTeX's stylesheet once; this component only produces the markup. A
// course that draws its own inline code (a mark before a name, say) supplies `code`; the
// platform renders the same words either way.
import Markdown, { type Components } from "react-markdown";
import rehypeKatex from "rehype-katex";
import remarkGfm from "remark-gfm";
import remarkMath from "remark-math";
import { useStrings } from "./StringsContext";

const REMARK = [remarkGfm, remarkMath];
const REHYPE = [rehypeKatex];

export function Prose({ markdown, className }: { markdown: string; className?: string }) {
  const strings = useStrings();
  return (
    <div className={className ? `prose ${className}` : "prose"}>
      <Markdown
        remarkPlugins={REMARK}
        rehypePlugins={REHYPE}
        components={strings.code ? ({ code: strings.code } as Components) : undefined}
      >
        {markdown}
      </Markdown>
    </div>
  );
}
