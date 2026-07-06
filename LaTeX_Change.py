import pyperclip
import re

def convert_latex_to_plain():
    text = pyperclip.paste()

    # 1. 数式の区切り文字や不要な縦線を削除
    text = text.replace('|', '').replace('｜', '')
    text = re.sub(r'\\\[|\\\]|\\\(|\\\)', '', text)
    text = text.replace('$', '')

    # 2. LaTeXコマンドを通常の記号に置換（le/ge などを追加・不等号を「≤」に統一）
    replacements = {
        # ギリシャ文字 (小文字)
        r'\alpha': 'α', r'\beta': 'β', r'\gamma': 'γ', r'\delta': 'δ', r'\epsilon': 'ε', r'\varepsilon': 'ε',
        r'\zeta': 'ζ', r'\eta': 'η', r'\theta': 'θ', r'\vartheta': 'ϑ', r'\iota': 'ι', r'\kappa': 'κ',
        r'\lambda': 'λ', r'\mu': 'μ', r'\nu': 'ν', r'\xi': 'ξ', r'\pi': 'π', r'\rho': 'ρ',
        r'\sigma': 'σ', r'\tau': 'τ', r'\upsilon': 'υ', r'\phi': 'φ', r'\varphi': 'φ', r'\chi': 'χ',
        r'\psi': 'ψ', r'\omega': 'ω',
        
        # ギリシャ文字 (大文字)
        r'\Gamma': 'Γ', r'\Delta': 'Δ', r'\Theta': 'Θ', r'\Lambda': 'Λ', r'\Xi': 'Ξ',
        r'\Pi': 'Π', r'\Sigma': 'Σ', r'\Upsilon': 'Υ', r'\Phi': 'Φ', r'\Psi': 'Ψ', r'\Omega': 'Ω',
        
        # 演算子・数学記号（le, ge などを追加）
        r'\times': '×', r'\div': '÷', r'\pm': '±', r'\mp': '∓', r'\cdot': '・', r'\ast': '＊', r'\circ': '∘',
        r'\neq': '≠', r'\leq': '≤', r'\le': '≤', r'\geq': '≥', r'\ge': '≥', r'\ll': '≪', r'\gg': '≫',
        r'\approx': '≈', r'\simeq': '≃', r'\equiv': '≡', r'\sim': '〜', r'\propto': '∝',
        
        # 集合・論理記号
        r'\in': '∈', r'\notin': '∉', r'\ni': '∋', r'\subset': '⊂', r'\supset': '⊃',
        r'\subseteq': '⊆', r'\supseteq': '⊇', r'\cup': '∪', r'\cap': '∩', r'\emptyset': '∅',
        r'\forall': '∀', r'\exists': '∃', r'\therefore': '∴', r'\because': '∵',
        
        # 矢印
        r'\Rightarrow': '⇒', r'\Leftarrow': '⇐', r'\Leftrightarrow': '⇔',
        r'\rightarrow': '→', r'\leftarrow': '←', r'\leftrightarrow': '↔', r'\to': '→',
        
        # 微積分・その他
        r'\infty': '∞', r'\nabla': '∇', r'\partial': '∂', r'\int': '∫', r'\iint': '∬', r'\oint': '∮',
        r'\angle': '∠', r'\triangle': '△', r'\square': '□', r'\sqrt': '√', r'\ell': 'ℓ', r'\dots': '...'
    }

    # 置換処理（文字数が長いコマンドから先に置換して誤変換を防ぐ）
    for latex_cmd in sorted(replacements.keys(), key=len, reverse=True):
        text = text.replace(latex_cmd, replacements[latex_cmd])

    # 3. \text{...} や \mathrm{...} のブロックを解除
    text = re.sub(r'\\text\s*\{([^}]+)\}', r'\1', text)
    text = re.sub(r'\\mathrm\s*\{([^}]+)\}', r'\1', text)
    text = re.sub(r'\\mathbf\s*\{([^}]+)\}', r'\1', text)

    # 4. 分数 \frac{A}{B} を (A)/(B) に変換
    text = re.sub(r'\\frac\s*\{([^}]+)\}\s*\{([^}]+)\}', r'(\1)/(\2)', text)

    # 5. 上付き・下付き文字の {} を外す (例: x^{2} -> x^2)
    text = re.sub(r'\^\s*\{([^}]+)\}', r'^\1', text)
    text = re.sub(r'_\s*\{([^}]+)\}', r'_\1', text)

    # 6. アンダースコア（下付き記号）を半角スペースに置換
    text = text.replace('_', ' ')

    # 7. 余ったバックスラッシュ(\)をすべて消去
    text = text.replace('\\', '')
    
    # 8. 変換しきれなかった波カッコ { } が残ってしまった場合のお掃除
    text = text.replace('{', '').replace('}', '')

    # 9. 連続する空白を1つにまとめ、前後の空白を消す
    text = re.sub(r'\s+', ' ', text).strip()

    # 整形したテキストをクリップボードに戻す
    pyperclip.copy(text)

    print("以下のテキストとしてクリップボードを更新しました：\n")
    print(text)

if __name__ == "__main__":
    convert_latex_to_plain()