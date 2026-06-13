"""Shared helpers for Phase Intervention Worksheet injection."""
import re


def score_color(val):
    if val == 'n/a':
        return '#6c757d'
    try:
        v = float(val)
        return '#27ae60' if v >= 80 else '#e67e22' if v >= 61.8 else '#c0392b'
    except Exception:
        return '#6c757d'


def axis_row(name, score, measures, if_below, category):
    c = score_color(score)
    s = str(score)
    return f"""          <tr>
            <td><strong>{name}</strong></td>
            <td style="font-weight:700;color:{c};">{s}</td>
            <td>{measures}</td>
            <td>{if_below}</td>
            <td>{category}</td>
          </tr>"""


def axis_table(pi, phi, sq2, ln2, e):
    rows = [
        axis_row('pi (π)', pi,
                 'Operational balance: chain average across all phases',
                 'Phases pulling the aggregate below the sustainable threshold',
                 'Process improvement; technology adoption at the phase level'),
        axis_row('phi (φ)', phi,
                 'Proportional value distribution: each phase receives value proportional to contribution',
                 'Value trapped or lost at phase transitions',
                 'Market structure reform; cooperative integration; direct-to-consumer models'),
        axis_row('sqrt2 (√2)', sq2,
                 'Structural overhead: physical or institutional friction raising D without adding C',
                 'Physical or regulatory constraints are the binding factor',
                 'Infrastructure investment; mechanisation; governance reform'),
        axis_row('ln2', ln2,
                 'Value transformation: how effectively each phase converts inputs to higher-value outputs',
                 'Transformation blocked by a gap (time lag, capital absence, biological delay)',
                 'Patient capital instruments; multi-cropping; phased transition'),
        axis_row('e', e,
                 'Financial abstraction: how well financial instruments are linked to real performance metrics',
                 'Available funding is not operationally connected to the ecosystem',
                 'Bond instrument design; KPI linkage; governance pre-conditions for finance activation'),
    ]
    return """    <table style="margin-top:12px;">
        <thead>
          <tr>
            <th>Constant</th><th>Chain Score</th><th>What It Measures</th>
            <th>If Below 80: The System Has...</th><th>Intervention Category</th>
          </tr>
        </thead>
        <tbody>
""" + '\n'.join(rows) + """
        </tbody>
      </table>"""


def bottleneck_block(phase_id, phase_name, balance, D, C, primary_axes, why_text,
                     interventions, combined_note):
    try:
        gap = round(float(D) - float(C), 3)
    except Exception:
        gap = 'n/a'
    rows = ''
    for rank, (iname, mech, proj) in enumerate(interventions, 1):
        rows += f"""          <tr>
            <td>{rank}</td>
            <td><strong>{iname}</strong></td>
            <td>{mech}</td>
            <td>{proj}</td>
          </tr>
"""
    return f"""    <!-- Phase {phase_id} intervention -->
    <div style="background:#fff;border-radius:10px;padding:20px;margin-bottom:16px;border:2px solid #e74c3c;">
      <div style="display:flex;align-items:center;gap:12px;margin-bottom:14px;">
        <div style="font-size:28px;font-weight:800;color:#e74c3c;">{phase_id}</div>
        <div>
          <div style="font-size:16px;font-weight:700;color:#1a1a1a;">{phase_name}</div>
          <div style="font-size:12px;color:#888;">Balance {balance}% | D={D}, C={C}, gap={gap} | Primary failure axis: <strong>{primary_axes}</strong></div>
        </div>
        <span style="margin-left:auto;background:#fde8e8;color:#8B1A1A;font-size:11px;font-weight:700;padding:4px 12px;border-radius:999px;text-transform:uppercase;">Bottleneck</span>
      </div>
      <p style="font-size:13px;color:#495057;margin-bottom:12px;">{why_text}</p>
      <table>
        <thead>
          <tr><th>Rank</th><th>Intervention</th><th>D-C Mechanism</th><th>Projected Balance</th></tr>
        </thead>
        <tbody>
{rows}        </tbody>
      </table>
      <p style="font-size:12px;color:#6c757d;margin-top:10px;font-style:italic;">{combined_note}</p>
    </div>"""


def worksheet(title, chain_bal, pi, phi, sq2, ln2, e, axis_note, blocks):
    table = axis_table(pi, phi, sq2, ln2, e)
    block_html = '\n'.join(blocks)
    return f"""
  <!-- Phase Intervention Worksheet -->
  <div class="section">
    <h2>Phase Intervention Worksheet</h2>
    <p style="font-size:13px;color:#6c757d;font-style:italic;margin-bottom:16px;">
      PROVISIONAL: Recommendations are derived analytically from PDI phase-level N-D-C data and public sources.
      Field validation is required before capital commitment. Each intervention is grounded in the specific
      mathematical axis that identifies the type of failure.
    </p>

    <div style="background:#fdf5f5;border-radius:10px;padding:20px;margin-bottom:20px;border-left:4px solid #8B1A1A;">
      <h3 style="margin-top:0;">How the Five-Model Constants Diagnose Failure: {title}</h3>
      <p>
        Each coherence axis (pi, phi, sqrt2, ln2, e) measures a different dimension of systemic health.
        The N-D-C balance formula is <strong>balance = 100 - (|D - C| / max(D, C)) * 100</strong>.
        A failing phase has D significantly greater than C: the constraint load exceeds contribution capacity.
        Chain average balance: <strong>{chain_bal}%</strong>.
      </p>
{table}
      <p style="font-size:12px;color:#6c757d;margin-top:10px;">{axis_note}</p>
    </div>

{block_html}
  </div>
"""


def inject(filepath, html):
    with open(filepath) as fh:
        text = fh.read()

    if 'Phase Intervention Worksheet' in text:
        print('SKIP (already has worksheet):', filepath)
        return

    for tag in ['</body>', '</main>']:
        idx = text.rfind(tag)
        if idx != -1:
            text = text[:idx] + html + '\n' + text[idx:]
            break

    with open(filepath, 'w') as fh:
        fh.write(text)
    print('OK:', filepath)


def inject_rebuild(filepath, html):
    """Replace existing worksheet or inject if missing."""
    with open(filepath) as fh:
        text = fh.read()

    if 'Phase Intervention Worksheet' in text:
        pattern = r'\s*<!-- Phase Intervention Worksheet -->.*?</div>(?=\s*\n\s*</div>|\s*\n\s*</body>|\s*\n\s*</main>)'
        text = re.sub(pattern, '', text, flags=re.DOTALL)

    for tag in ['</body>', '</main>']:
        idx = text.rfind(tag)
        if idx != -1:
            text = text[:idx] + html + '\n' + text[idx:]
            break

    with open(filepath, 'w') as fh:
        fh.write(text)
    print('REBUILT:', filepath)
