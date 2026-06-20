(function (root, factory) {
  const api = factory();
  if (typeof module === "object" && module.exports) module.exports = api;
  root.LiuyaoEngine = api;
})(typeof globalThis !== "undefined" ? globalThis : window, function () {
  const YAOS = ["111", "110", "101", "100", "011", "010", "001", "000"];
  const GUAS = ["乾", "兑", "离", "震", "巽", "坎", "艮", "坤"];
  const ELEMENTS = ["木", "火", "土", "金", "水"];
  const GUA_ELEMENT_INDEX = [3, 3, 1, 0, 0, 4, 2, 2];
  const SIX_RELATIVES = ["兄弟", "父母", "官鬼", "妻财", "子孙"];
  const GANS = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"];

  const TRIGRAMS = {
    "111": { name: "乾", element: "金" },
    "110": { name: "兑", element: "金" },
    "101": { name: "离", element: "火" },
    "100": { name: "震", element: "木" },
    "011": { name: "巽", element: "木" },
    "010": { name: "坎", element: "水" },
    "001": { name: "艮", element: "土" },
    "000": { name: "坤", element: "土" },
  };

  const GUA64 = {
    "111111": "乾为天",
    "011111": "天风姤",
    "001111": "天山遁",
    "000111": "天地否",
    "000011": "风地观",
    "000001": "山地剥",
    "000101": "火地晋",
    "111101": "火天大有",
    "110110": "兑为泽",
    "010110": "泽水困",
    "000110": "泽地萃",
    "001110": "泽山咸",
    "001010": "水山蹇",
    "001000": "地山谦",
    "001100": "雷山小过",
    "110100": "雷泽归妹",
    "101101": "离为火",
    "001101": "火山旅",
    "011101": "火风鼎",
    "010101": "火水未济",
    "010001": "山水蒙",
    "010011": "风水涣",
    "010111": "天水讼",
    "101111": "天火同人",
    "100100": "震为雷",
    "000100": "雷地豫",
    "010100": "雷水解",
    "011100": "雷风恒",
    "011000": "地风升",
    "011010": "水风井",
    "011110": "泽风大过",
    "100110": "泽雷随",
    "011011": "巽为风",
    "111011": "风天小畜",
    "101011": "风火家人",
    "100011": "风雷益",
    "100111": "天雷无妄",
    "100101": "火雷噬嗑",
    "100001": "山雷颐",
    "011001": "山风蛊",
    "010010": "坎为水",
    "110010": "水泽节",
    "100010": "水雷屯",
    "101010": "水火既济",
    "101110": "泽火革",
    "101100": "雷火丰",
    "101000": "地火明夷",
    "010000": "地水师",
    "001001": "艮为山",
    "101001": "山火贲",
    "111001": "山天大畜",
    "110001": "山泽损",
    "110101": "火泽睽",
    "110111": "天泽履",
    "110011": "风泽中孚",
    "001011": "风山渐",
    "000000": "坤为地",
    "100000": "地雷复",
    "110000": "地泽临",
    "111000": "地天泰",
    "111100": "雷天大壮",
    "111110": "泽天夬",
    "111010": "水天需",
    "000010": "水地比",
  };

  const NAJIA = [
    ["甲子寅辰", "壬午申戌"],
    ["丁巳卯丑", "丁亥酉未"],
    ["己卯丑亥", "己酉未巳"],
    ["庚子寅辰", "庚午申戌"],
    ["辛丑亥酉", "辛未巳卯"],
    ["戊寅辰午", "戊申戌子"],
    ["丙辰午申", "丙戌子寅"],
    ["乙未巳卯", "癸丑亥酉"],
  ];

  const ZHIS = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"];
  const ZHI_ELEMENT_INDEX = [4, 2, 0, 0, 2, 1, 1, 2, 3, 3, 2, 4];
  const VOID_BRANCHES = ["子丑", "寅卯", "辰巳", "午未", "申酉", "戌亥"];
  const CLASHES = {
    子: "午",
    丑: "未",
    寅: "申",
    卯: "酉",
    辰: "戌",
    巳: "亥",
    午: "子",
    未: "丑",
    申: "寅",
    酉: "卯",
    戌: "辰",
    亥: "巳",
  };

  const SIX_SPIRIT_START = {
    甲: 0,
    乙: 0,
    丙: 1,
    丁: 1,
    戊: 2,
    己: 3,
    庚: 4,
    辛: 4,
    壬: 5,
    癸: 5,
  };
  const SIX_SPIRITS = ["青龙", "朱雀", "勾陈", "螣蛇", "白虎", "玄武"];

  const GENERATES = {
    木: "火",
    火: "土",
    土: "金",
    金: "水",
    水: "木",
  };
  const CONTROLS = {
    木: "土",
    土: "水",
    水: "火",
    火: "金",
    金: "木",
  };

  const PALACE_SEQUENCES = [
    ["111111", "011111", "001111", "000111", "000011", "000001", "000101", "111101"],
    ["110110", "010110", "000110", "001110", "001010", "001000", "001100", "110100"],
    ["101101", "001101", "011101", "010101", "010001", "010011", "010111", "101111"],
    ["100100", "000100", "010100", "011100", "011000", "011010", "011110", "100110"],
    ["011011", "111011", "101011", "100011", "100111", "100101", "100001", "011001"],
    ["010010", "110010", "100010", "101010", "101110", "101100", "101000", "010000"],
    ["001001", "101001", "111001", "110001", "110101", "110111", "110011", "001011"],
    ["000000", "100000", "110000", "111000", "111100", "111110", "111010", "000010"],
  ];

  const PALACE_LOOKUP = new Map();
  PALACE_SEQUENCES.forEach((sequence, palaceIndex) => {
    sequence.forEach((mark, generationIndex) => {
      PALACE_LOOKUP.set(mark, { palaceIndex, generationIndex });
    });
  });

  function normalizeLine(value) {
    const normalized = String(value).trim();
    const map = {
      "6": { yinYang: "yin", moving: true, value: 6, label: "老阴" },
      "7": { yinYang: "yang", moving: false, value: 7, label: "少阳" },
      "8": { yinYang: "yin", moving: false, value: 8, label: "少阴" },
      "9": { yinYang: "yang", moving: true, value: 9, label: "老阳" },
      old_yin: { yinYang: "yin", moving: true, value: 6, label: "老阴" },
      young_yang: { yinYang: "yang", moving: false, value: 7, label: "少阳" },
      young_yin: { yinYang: "yin", moving: false, value: 8, label: "少阴" },
      old_yang: { yinYang: "yang", moving: true, value: 9, label: "老阳" },
      yin: { yinYang: "yin", moving: false, value: 8, label: "少阴" },
      yang: { yinYang: "yang", moving: false, value: 7, label: "少阳" },
    };
    return map[normalized] || null;
  }

  function lineBit(line) {
    return line.yinYang === "yang" ? "1" : "0";
  }

  function changedLine(line) {
    if (!line.moving) return line;
    return line.yinYang === "yang"
      ? { yinYang: "yin", moving: false, value: 8, label: "少阴" }
      : { yinYang: "yang", moving: false, value: 7, label: "少阳" };
  }

  function trigramFromLines(lines) {
    const key = lines.map(lineBit).join("");
    return { key, ...TRIGRAMS[key] };
  }

  function markFromLines(lines) {
    return lines.map(lineBit).join("");
  }

  function hexagramFromLines(lines) {
    const lower = trigramFromLines(lines.slice(0, 3));
    const upper = trigramFromLines(lines.slice(3, 6));
    const mark = markFromLines(lines);
    return {
      name: GUA64[mark] || `${upper.name}${lower.name}`,
      lower,
      upper,
      mark,
      binary: mark,
    };
  }

  function sixSpiritFor(dayStem, lineIndex) {
    const start = SIX_SPIRIT_START[String(dayStem || "").trim()];
    if (start === undefined) return "";
    return SIX_SPIRITS[(start + lineIndex) % SIX_SPIRITS.length];
  }

  function sixRelative(palaceElement, lineElement) {
    if (!ELEMENTS.includes(palaceElement) || !ELEMENTS.includes(lineElement)) return "";
    if (lineElement === palaceElement) return "兄弟";
    if (GENERATES[palaceElement] === lineElement) return "子孙";
    if (CONTROLS[palaceElement] === lineElement) return "妻财";
    if (GENERATES[lineElement] === palaceElement) return "父母";
    if (CONTROLS[lineElement] === palaceElement) return "官鬼";
    return "";
  }

  function sixRelativeByIndex(palaceElement, lineElement) {
    const palaceIndex = ELEMENTS.indexOf(palaceElement);
    const lineIndex = ELEMENTS.indexOf(lineElement);
    if (palaceIndex < 0 || lineIndex < 0) return "";
    return SIX_RELATIVES[(palaceIndex - lineIndex + 5) % 5];
  }

  function getSoulType(mark) {
    const outer = mark.slice(3);
    const inner = mark.slice(0, 3);
    if (outer[1] === inner[1] && outer[0] !== inner[0] && outer[2] !== inner[2]) return "游魂";
    if (outer[1] !== inner[1] && outer[0] === inner[0] && outer[2] === inner[2]) return "归魂";
    return "";
  }

  function autoWorldResponse(mark) {
    const match = PALACE_LOOKUP.get(mark);
    if (!match) return { shiLine: 0, yingLine: 0, generationIndex: -1 };
    const worldByGeneration = [6, 1, 2, 3, 4, 5, 4, 3];
    const shiLine = worldByGeneration[match.generationIndex];
    const yingLine = shiLine > 3 ? shiLine - 3 : shiLine + 3;
    return { shiLine, yingLine, generationIndex: match.generationIndex };
  }

  function palaceForMark(mark) {
    const match = PALACE_LOOKUP.get(mark);
    if (!match) return { index: -1, name: "", element: "", pureMark: "" };
    const element = ELEMENTS[GUA_ELEMENT_INDEX[match.palaceIndex]];
    return {
      index: match.palaceIndex,
      name: GUAS[match.palaceIndex],
      element,
      pureMark: PALACE_SEQUENCES[match.palaceIndex][0],
    };
  }

  function getNajia(mark) {
    const innerIndex = YAOS.indexOf(mark.slice(0, 3));
    const outerIndex = YAOS.indexOf(mark.slice(3, 6));
    if (innerIndex < 0 || outerIndex < 0) return [];

    const inner = NAJIA[innerIndex][0];
    const outer = NAJIA[outerIndex][1];
    const innerStem = inner[0];
    const outerStem = outer[0];
    return [
      ...inner
        .slice(1)
        .split("")
        .map((branch) => `${innerStem}${branch}`),
      ...outer
        .slice(1)
        .split("")
        .map((branch) => `${outerStem}${branch}`),
    ];
  }

  function branchElement(ganzhi) {
    const branch = String(ganzhi || "")[1];
    const index = ZHIS.indexOf(branch);
    if (index < 0) return "";
    return ELEMENTS[ZHI_ELEMENT_INDEX[index]];
  }

  function elementForBranch(branch) {
    const index = ZHIS.indexOf(String(branch || "").trim());
    if (index < 0) return "";
    return ELEMENTS[ZHI_ELEMENT_INDEX[index]];
  }

  function branchFromGanzhi(ganzhi) {
    const value = String(ganzhi || "").trim();
    return value.length >= 2 && ZHIS.includes(value[1]) ? value[1] : "";
  }

  function calculateVoidBranches(dayGanzhi) {
    const value = String(dayGanzhi || "").trim();
    const stem = value[0];
    const branch = value[1];
    const stemIndex = GANS.indexOf(stem);
    let branchIndex = ZHIS.indexOf(branch);
    if (stemIndex < 0 || branchIndex < 0) return [];
    if (stemIndex === branchIndex || branchIndex < stemIndex) branchIndex += 12;
    const voidIndex = Math.floor((branchIndex - stemIndex) / 2) - 1;
    return (VOID_BRANCHES[voidIndex] || "").split("");
  }

  function branchRelation(sourceBranch, targetBranch) {
    const source = String(sourceBranch || "").trim();
    const target = String(targetBranch || "").trim();
    if (!source || !target) return "";
    if (CLASHES[source] === target) return "冲";
    const sourceElement = elementForBranch(source);
    const targetElement = elementForBranch(target);
    if (!sourceElement || !targetElement) return "";
    if (sourceElement === targetElement) return "同";
    if (GENERATES[sourceElement] === targetElement) return "生";
    if (CONTROLS[sourceElement] === targetElement) return "克";
    if (GENERATES[targetElement] === sourceElement) return "泄";
    if (CONTROLS[targetElement] === sourceElement) return "受克";
    return "";
  }

  function statusFromRelation(prefix, relation) {
    if (!relation) return "";
    if (relation === "冲") return `${prefix}冲`;
    if (relation === "同") return `${prefix}同`;
    if (relation === "生") return `${prefix}生`;
    if (relation === "克") return `${prefix}克`;
    if (relation === "泄") return `${prefix}泄`;
    if (relation === "受克") return `${prefix}受克`;
    return "";
  }

  function hiddenGods(palace, relatives) {
    if (!palace || palace.index < 0 || new Set(relatives).size >= 5) return null;
    const palaceMark = palace.pureMark;
    const pureNajia = getNajia(palaceMark);
    const pureLines = pureNajia.map((ganzhi, index) => {
      const element = branchElement(ganzhi);
      return {
        line: index + 1,
        ganzhi,
        element,
        relative: sixRelativeByIndex(palace.element, element),
      };
    });
    const missingRelatives = SIX_RELATIVES.filter((relative) => !relatives.includes(relative))
      .map((relative) => pureLines.find((line) => line.relative === relative))
      .filter(Boolean);

    if (!missingRelatives.length) return null;
    return {
      palaceHexagram: GUA64[palaceMark],
      mark: palaceMark,
      missingRelatives,
      lines: pureLines,
    };
  }

  function validateLiuyaoInput(input) {
    const errors = [];
    if (!Array.isArray(input.lines) || input.lines.length !== 6) {
      errors.push("lines must contain 6 items from bottom line to top line");
    }
    const lines = Array.isArray(input.lines) ? input.lines.map(normalizeLine) : [];
    if (lines.some((line) => !line)) {
      errors.push("line values must be 6/7/8/9 or old_yin/young_yang/young_yin/old_yang");
    }
    if (input.dayStem && SIX_SPIRIT_START[String(input.dayStem).trim()] === undefined) {
      errors.push("dayStem must be one of 甲乙丙丁戊己庚辛壬癸");
    }
    if (input.dayGanzhi) {
      const value = String(input.dayGanzhi).trim();
      if (!GANS.includes(value[0]) || !ZHIS.includes(value[1])) {
        errors.push("dayGanzhi must be a valid stem-branch such as 甲子");
      }
    }
    if (input.monthBranch && !ZHIS.includes(String(input.monthBranch).trim())) {
      errors.push("monthBranch must be one of 子丑寅卯辰巳午未申酉戌亥");
    }
    return { ok: errors.length === 0, errors };
  }

  function buildLiuyaoChart(input) {
    const validation = validateLiuyaoInput(input);
    if (!validation.ok) {
      const error = new Error(validation.errors.join("; "));
      error.errors = validation.errors;
      throw error;
    }

    const normalized = input.lines.map(normalizeLine);
    const changed = normalized.map(changedLine);
    const primary = hexagramFromLines(normalized);
    const changedHexagram = hexagramFromLines(changed);
    const autoLines = autoWorldResponse(primary.mark);
    const palace = palaceForMark(primary.mark);
    const palaceElement = input.palaceElement || palace.element;
    const najia = getNajia(primary.mark);
    const lineElements = najia.map(branchElement);
    const lineBranches = najia.map(branchFromGanzhi);
    const relatives = lineElements.map((element, index) =>
      sixRelativeByIndex(palaceElement, input.lineElements?.[index] || element),
    );
    const dayGanzhi = String(input.dayGanzhi || "").trim();
    const dayStem = String(input.dayStem || dayGanzhi[0] || "").trim();
    const dayBranch = branchFromGanzhi(dayGanzhi);
    const monthBranch = String(input.monthBranch || "").trim();
    const voidBranches = calculateVoidBranches(dayGanzhi);
    const shiLine = Number(input.shiLine) || autoLines.shiLine;
    const yingLine = Number(input.yingLine) || autoLines.yingLine;
    const movingLines = normalized
      .map((line, index) => (line.moving ? index + 1 : null))
      .filter(Boolean);

    return {
      primary,
      changed: changedHexagram,
      palace,
      palaceElement,
      soul: getSoulType(primary.mark),
      generationIndex: autoLines.generationIndex,
      time: {
        dayGanzhi,
        dayStem,
        dayBranch,
        monthBranch,
        voidBranches,
      },
      shiLine,
      yingLine,
      movingLines,
      hidden: hiddenGods({ ...palace, element: palaceElement }, relatives),
      lines: normalized.map((line, index) => ({
        index: index + 1,
        value: line.value,
        label: line.label,
        yinYang: line.yinYang,
        moving: line.moving,
        changedTo: changed[index].label,
        sixSpirit: sixSpiritFor(dayStem, index),
        ganzhi: najia[index] || "",
        branch: lineBranches[index] || "",
        element: input.lineElements?.[index] || lineElements[index] || "",
        sixRelative: relatives[index],
        void: voidBranches.includes(lineBranches[index]),
        voidLabel: voidBranches.includes(lineBranches[index]) ? "旬空" : "",
        dayStatus: statusFromRelation("日", branchRelation(dayBranch, lineBranches[index])),
        monthStatus: statusFromRelation("月", branchRelation(monthBranch, lineBranches[index])),
        role: shiLine === index + 1 ? "世" : yingLine === index + 1 ? "应" : "",
      })),
    };
  }

  return {
    buildLiuyaoChart,
    validateLiuyaoInput,
    sixRelative,
    sixRelativeByIndex,
    sixSpiritFor,
    calculateVoidBranches,
    branchRelation,
    getNajia,
  };
});
