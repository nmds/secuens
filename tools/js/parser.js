/**
 * Secuens Reference Parser — JavaScript / Node.js
 * Version: 0.9.1
 * License: MIT (tool implementation; specification under CC BY-ND 4.0)
 *
 * A minimal reference parser for the Secuens specification v0.9.1.
 * Works in Node.js and in modern browsers (no dependencies).
 *
 * Usage (Node.js CLI):
 *   node parser.js script.secuens
 *   node parser.js script.fountain
 *
 * Usage (Node.js module):
 *   const { SecuensParser } = require('./parser');
 *   const parser = new SecuensParser();
 *   const result = parser.parseText(scriptText);
 *   // result.cues        — array of parsed cues
 *   // result.warnings    — array of non-fatal warnings
 *   // result.cueTypesSeen — map of cuetype -> label
 *
 * Usage (browser):
 *   <script src="parser.js"></script>
 *   <script>
 *     const parser = new SecuensParser();
 *     const result = parser.parseText(scriptText);
 *     // result.cues        — array of parsed cues
 *     // result.warnings    — array of non-fatal warnings
 *     // result.cueTypesSeen — map of cuetype -> label
 *   </script>
 */

'use strict';

// ---------------------------------------------------------------------------
// Regex Patterns
// ---------------------------------------------------------------------------

const BONEYARD_RE = /^\[\[(.*)\]\]$/;
const FORCED_ACTION_RE = /^!/;

/**
 * Core cue pattern.
 * Groups: [1] cuetype, [2] label, [3] number, [4] trigger, [5] metadata, [6] description
 */
const CUE_RE = /^([A-Z]+)\s*\(([a-z]+)\s+([A-Z]?[0-9]+(?:[a-z]*|\.[0-9]+))\s*\)(?:\s+([a-z]+\s+(?:"[^"]*"|[0-9]+(?:\.[0-9]+)?(?:s|m|ms|h)|[^"[\n][^[:\n]*?)))?(?:\s*\[([^\]]*)\])?\s*:\s*(.*)/;

/** Detects trigger keyword immediately before colon (no value) */
const TRIGGER_NO_VALUE_RE = /^([A-Z]+)\s*\([a-z]+\s+[^)]+\)\s+([a-z]+)\s*(?:\[[^\]]*\])?\s*:/;

/** Metadata key=value pair */
const METADATA_PAIR_RE = /([a-z]+)=((?:"[^"]*"|[^,\]]+))/g;

/** Time value with required units */
const TIME_VALUE_RE = /^[0-9]+(?:\.[0-9]+)?(s|m|ms|h)$/;

const TIME_KEYS = new Set(['duration', 'fade', 'prewait', 'postwait', 'warn']);

// ---------------------------------------------------------------------------
// Parser
// ---------------------------------------------------------------------------

class SecuensParser {

  /**
   * Parse a plain text string containing a Secuens document.
   * @param {string} text
   * @returns {ParseResult}
   */
  parseText(text) {
    const lines = text.split(/\r?\n/);
    return this._parseLines(lines);
  }

  /**
   * Parse an array of lines.
   * @param {string[]} lines
   * @returns {ParseResult}
   */
  _parseLines(lines) {
    const cues = [];
    const warnings = [];
    const cueTypesSeen = {}; // cuetype -> label

    lines.forEach((rawLine, index) => {
      const lineNumber = index + 1;
      let line = rawLine.trimEnd();

      // Check for Fountain boneyard (hidden cues)
      let hidden = false;
      const boneyardMatch = line.match(BONEYARD_RE);
      if (boneyardMatch) {
        line = boneyardMatch[1].trim();
        hidden = true;
      }

      // Strip forced action prefix
      line = line.replace(FORCED_ACTION_RE, '');

      // Attempt to parse as a cue
      const cue = this._parseCue(line, lineNumber, rawLine.trimEnd(), hidden, warnings);
      if (!cue) return;

      // Check label consistency (SHOULD warn)
      const existingLabel = cueTypesSeen[cue.cueType];
      if (existingLabel === undefined) {
        cueTypesSeen[cue.cueType] = cue.label;
      } else if (existingLabel !== cue.label) {
        warnings.push({
          lineNumber,
          message: `Inconsistent label for ${cue.cueType}: previously '${existingLabel}', now '${cue.label}'`,
          raw: rawLine.trimEnd()
        });
      }

      cues.push(cue);
    });

    // Check for duplicates (SHOULD warn)
    this._checkDuplicates(cues, warnings);

    return { cues, warnings, cueTypesSeen };
  }

  _parseCue(line, lineNumber, raw, hidden, warnings) {
    // Check for trigger-keyword-without-value
    const kwNoVal = line.match(TRIGGER_NO_VALUE_RE);
    if (kwNoVal) {
      warnings.push({
        lineNumber,
        message: `Trigger keyword '${kwNoVal[2]}' has no value`,
        raw
      });
    }

    const match = line.match(CUE_RE);
    if (!match) return null;

    const [, cueType, label, number, triggerRaw, metadataRaw, descriptionRaw] = match;
    const description = descriptionRaw.trim();

    // Parse trigger
    let triggerKeyword = null;
    let triggerValue = null;
    if (triggerRaw) {
      const triggerParts = triggerRaw.trim().split(/\s+(.+)/);
      if (triggerParts.length >= 2) {
        triggerKeyword = triggerParts[0];
        triggerValue = triggerParts[1];
      } else {
        triggerKeyword = triggerParts[0];
        warnings.push({
          lineNumber,
          message: `Trigger keyword '${triggerKeyword}' has no value`,
          raw
        });
      }
    }

    // Parse metadata
    let metadata = {};
    if (metadataRaw) {
      const { pairs, metaWarnings } = this._parseMetadata(metadataRaw, lineNumber, raw);
      metadata = pairs;
      warnings.push(...metaWarnings);
    }

    // Warn on empty description
    if (!description) {
      warnings.push({
        lineNumber,
        message: `${cueType} (${label} ${number}): Missing description — treating as placeholder`,
        raw
      });
    }

    return {
      lineNumber,
      raw,
      cueType,
      label,
      number,
      description,
      triggerKeyword,
      triggerValue,
      metadata,
      hidden
    };
  }

  _parseMetadata(metadataRaw, lineNumber, raw) {
    const pairs = {};
    const metaWarnings = [];
    let match;

    METADATA_PAIR_RE.lastIndex = 0;
    while ((match = METADATA_PAIR_RE.exec(metadataRaw)) !== null) {
      const key = match[1];
      let value = match[2].trim();

      // Strip quotes
      if (value.startsWith('"') && value.endsWith('"')) {
        value = value.slice(1, -1);
      }

      // Validate time units
      if (TIME_KEYS.has(key)) {
        const descriptive = ['slow', 'fast', 'instant'];
        if (!TIME_VALUE_RE.test(value) && !descriptive.includes(value)) {
          metaWarnings.push({
            lineNumber,
            message: `Time value '${value}' for key '${key}' missing units (expected: s, m, ms, h)`,
            raw
          });
        }
      }

      pairs[key] = value;
    }

    return { pairs, metaWarnings };
  }

  _checkDuplicates(cues, warnings) {
    const seen = {}; // "CUETYPE:number" -> lineNumber
    for (const cue of cues) {
      const key = `${cue.cueType}:${cue.number}`;
      if (key in seen) {
        warnings.push({
          lineNumber: cue.lineNumber,
          message: `Duplicate cue number: ${cue.cueType} ${cue.label} ${cue.number} (first seen at line ${seen[key]})`,
          raw: cue.raw
        });
      } else {
        seen[key] = cue.lineNumber;
      }
    }
  }
}

// ---------------------------------------------------------------------------
// CLI (Node.js only)
// ---------------------------------------------------------------------------

function formatResult(filepath, result) {
  const lines = [];
  lines.push(`Secuens Parser v0.9.1 — ${filepath}`);
  lines.push('─'.repeat(60));
  lines.push(`Found ${result.cues.length} cue(s), ${result.warnings.length} warning(s)`);
  lines.push('');

  for (const cue of result.cues) {
    const hiddenMark = cue.hidden ? ' [HIDDEN]' : '';
    const triggerStr = cue.triggerKeyword ? ` | trigger: ${cue.triggerKeyword} ${cue.triggerValue}` : '';
    const metaStr = Object.keys(cue.metadata).length
      ? ` | metadata: ${JSON.stringify(cue.metadata)}`
      : '';
    lines.push(`  Line ${String(cue.lineNumber).padStart(4)}${hiddenMark}: ${cue.cueType} (${cue.label} ${cue.number})${triggerStr}${metaStr}`);
    if (cue.description) {
      lines.push(`             → ${cue.description}`);
    }
  }

  if (result.warnings.length) {
    lines.push('');
    lines.push('Warnings:');
    for (const w of result.warnings) {
      lines.push(`  Line ${String(w.lineNumber).padStart(4)}: ⚠ ${w.message}`);
    }
  }

  lines.push('');
  lines.push('Cue Types:');
  const typeEntries = Object.entries(result.cueTypesSeen).sort();
  for (const [cueType, label] of typeEntries) {
    const count = result.cues.filter(c => c.cueType === cueType).length;
    lines.push(`  ${cueType.padEnd(12)} (${label}) — ${count} cue(s)`);
  }

  return lines.join('\n');
}

if (typeof require !== 'undefined' && require.main === module) {
  const fs = require('fs');
  const filepath = process.argv[2];

  if (!filepath) {
    console.error('Usage: node parser.js <file.secuens>');
    process.exit(1);
  }

  let text;
  try {
    text = fs.readFileSync(filepath, 'utf-8');
  } catch (e) {
    console.error(`Error: File not found: ${filepath}`);
    process.exit(1);
  }

  const parser = new SecuensParser();
  const result = parser.parseText(text);
  console.log(formatResult(filepath, result));
}

// ---------------------------------------------------------------------------
// Export
// ---------------------------------------------------------------------------

if (typeof module !== 'undefined') {
  module.exports = { SecuensParser };
}
