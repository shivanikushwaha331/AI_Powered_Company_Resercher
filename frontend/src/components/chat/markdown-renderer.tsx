import React, { useState } from "react";

interface MarkdownRendererProps {
  content: string;
}

export function MarkdownRenderer({ content }: MarkdownRendererProps) {
  if (!content) return null;

  // Split content into blocks (code blocks, tables, headings, paragraphs)
  const blocks = parseMarkdownBlocks(content);

  return (
    <div className="space-y-3 text-sm leading-relaxed text-foreground">
      {blocks.map((block, idx) => {
        if (block.type === "code") {
          return <CodeBlock key={idx} language={block.language || ""} code={block.text} />;
        } else if (block.type === "table") {
          return <TableBlock key={idx} rows={block.tableRows || []} />;
        } else if (block.type === "h1") {
          return (
            <h1 key={idx} className="text-xl font-bold tracking-tight text-foreground pt-2 pb-1 border-b border-border/50">
              {block.text}
            </h1>
          );
        } else if (block.type === "h2") {
          return (
            <h2 key={idx} className="text-lg font-bold tracking-tight text-primary pt-2 pb-0.5">
              {block.text}
            </h2>
          );
        } else if (block.type === "h3") {
          return (
            <h3 key={idx} className="text-base font-semibold text-foreground pt-1">
              {block.text}
            </h3>
          );
        } else if (block.type === "ul") {
          return (
            <ul key={idx} className="list-disc list-inside space-y-1 pl-1 text-muted-foreground">
              {block.items?.map((item, i) => (
                <li key={i} className="text-foreground">
                  {renderInlineFormatting(item)}
                </li>
              ))}
            </ul>
          );
        } else if (block.type === "ol") {
          return (
            <ol key={idx} className="list-decimal list-inside space-y-1 pl-1 text-muted-foreground">
              {block.items?.map((item, i) => (
                <li key={i} className="text-foreground">
                  {renderInlineFormatting(item)}
                </li>
              ))}
            </ol>
          );
        }

        return <p key={idx}>{renderInlineFormatting(block.text)}</p>;
      })}
    </div>
  );
}

// Inline formatting helper for Bold (**text**) and Italic (*text*)
function renderInlineFormatting(text: string) {
  const parts = text.split(/(\*\*.*?\*\*|\*.*?\*|`.*?`)/g);
  return parts.map((part, i) => {
    if (part.startsWith("**") && part.endsWith("**")) {
      return <strong key={i} className="font-bold text-foreground">{part.slice(2, -2)}</strong>;
    } else if (part.startsWith("*") && part.endsWith("*")) {
      return <em key={i} className="italic text-muted-foreground">{part.slice(1, -1)}</em>;
    } else if (part.startsWith("`") && part.endsWith("`")) {
      return (
        <code key={i} className="px-1.5 py-0.5 rounded bg-muted text-primary font-mono text-xs">
          {part.slice(1, -1)}
        </code>
      );
    }
    return part;
  });
}

// Code Block Component with Copy Code Button
function CodeBlock({ language, code }: { language: string; code: string }) {
  const [copied, setCopied] = useState(false);

  const handleCopy = () => {
    navigator.clipboard.writeText(code);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="my-3 rounded-xl border border-border bg-slate-950 text-slate-100 overflow-hidden shadow-lg font-mono text-xs">
      <div className="flex items-center justify-between px-4 py-2 border-b border-slate-800 bg-slate-900/80 text-[11px] text-slate-400">
        <span>{language || "code"}</span>
        <button
          onClick={handleCopy}
          className="hover:text-slate-100 transition-colors flex items-center gap-1"
        >
          {copied ? "✓ Copied" : "📋 Copy code"}
        </button>
      </div>
      <pre className="p-4 overflow-x-auto leading-relaxed">
        <code>{code}</code>
      </pre>
    </div>
  );
}

// Table Block Component
function TableBlock({ rows }: { rows: string[][] }) {
  if (rows.length === 0) return null;
  const header = rows[0];
  const body = rows.slice(1);

  return (
    <div className="my-3 overflow-x-auto rounded-xl border border-border bg-card shadow-sm">
      <table className="w-full text-left border-collapse text-xs">
        <thead>
          <tr className="border-b border-border bg-secondary/50 font-bold text-foreground">
            {header.map((col, i) => (
              <th key={i} className="p-3">
                {col}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {body.map((row, rIdx) => (
            <tr key={rIdx} className="border-b border-border/40 hover:bg-muted/30 transition-colors">
              {row.map((cell, cIdx) => (
                <td key={cIdx} className="p-3">
                  {cell}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

// Block Parser Helper
interface Block {
  type: "p" | "h1" | "h2" | "h3" | "ul" | "ol" | "code" | "table";
  text: string;
  language?: string;
  items?: string[];
  tableRows?: string[][];
}

function parseMarkdownBlocks(rawText: string): Block[] {
  const lines = rawText.split("\n");
  const blocks: Block[] = [];
  let inCode = false;
  let codeLang = "";
  let codeBuffer: string[] = [];
  let listBuffer: string[] = [];
  let isNumbered = false;
  let tableBuffer: string[][] = [];

  const flushList = () => {
    if (listBuffer.length > 0) {
      blocks.push({
        type: isNumbered ? "ol" : "ul",
        text: "",
        items: [...listBuffer],
      });
      listBuffer = [];
    }
  };

  const flushTable = () => {
    if (tableBuffer.length > 0) {
      blocks.push({
        type: "table",
        text: "",
        tableRows: [...tableBuffer],
      });
      tableBuffer = [];
    }
  };

  for (let line of lines) {
    const trimmed = line.trim();

    // Code Block Toggle
    if (trimmed.startsWith("```")) {
      if (inCode) {
        blocks.push({
          type: "code",
          text: codeBuffer.join("\n"),
          language: codeLang,
        });
        codeBuffer = [];
        inCode = false;
      } else {
        flushList();
        flushTable();
        inCode = true;
        codeLang = trimmed.replace("```", "").trim();
      }
      continue;
    }

    if (inCode) {
      codeBuffer.push(line);
      continue;
    }

    // Markdown Table Line (| Col 1 | Col 2 |)
    if (trimmed.startsWith("|") && trimmed.endsWith("|")) {
      flushList();
      if (trimmed.includes("---")) continue; // Skip separator line
      const cells = trimmed
        .split("|")
        .slice(1, -1)
        .map((c) => c.trim());
      tableBuffer.push(cells);
      continue;
    } else if (tableBuffer.length > 0) {
      flushTable();
    }

    // Headings
    if (trimmed.startsWith("# ")) {
      flushList();
      blocks.push({ type: "h1", text: trimmed.substring(2) });
      continue;
    } else if (trimmed.startsWith("## ")) {
      flushList();
      blocks.push({ type: "h2", text: trimmed.substring(3) });
      continue;
    } else if (trimmed.startsWith("### ")) {
      flushList();
      blocks.push({ type: "h3", text: trimmed.substring(4) });
      continue;
    }

    // Bullet Lists (- or *)
    if (trimmed.startsWith("- ") || trimmed.startsWith("* ")) {
      if (isNumbered) flushList();
      isNumbered = false;
      listBuffer.push(trimmed.substring(2));
      continue;
    }

    // Numbered Lists (1.)
    if (/^\d+\.\s/.test(trimmed)) {
      if (!isNumbered) flushList();
      isNumbered = true;
      listBuffer.push(trimmed.replace(/^\d+\.\s/, ""));
      continue;
    }

    // Empty line or standard paragraph
    if (!trimmed) {
      flushList();
      continue;
    }

    flushList();
    blocks.push({ type: "p", text: trimmed });
  }

  flushList();
  flushTable();

  return blocks;
}
