"""
Blender 4/5 Python script — Regular tetrahedron with per-face UV islands and materials.

Run with:
    blender --background --python make_tetrahedron.py

The script:
  • Constructs a regular tetrahedron inscribed in the unit sphere
  • Assigns 4 named materials (bottom / front / left / right), one per face
  • Maps each face to an upright full-UV-space triangle island (0-1 range)
  • Loads matching PNG textures from the script's own directory
  • Adds camera + sun light with a clear view of the front face
  • Saves tetrahedron_uv.blend alongside this script
"""

import bpy
import bmesh
import math
import os

# ── paths ─────────────────────────────────────────────────────────────────────

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_BLEND  = os.path.join(SCRIPT_DIR, "tetrahedron_uv.blend")

# ── clear scene ───────────────────────────────────────────────────────────────

bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
for col in (bpy.data.meshes, bpy.data.materials,
            bpy.data.images, bpy.data.cameras, bpy.data.lights):
    for item in list(col):
        col.remove(item)

# ── regular tetrahedron vertices (inscribed in unit sphere) ───────────────────
#
#   v0 = apex (top, +Z)
#   v1 = back base vertex  (+Y, behind the "front" face)
#   v2 = left base vertex  (-X, -Y)
#   v3 = right base vertex (+X, -Y)
#
#   Face normals (outward):
#     (v1,v3,v2) → (0, 0, −1)  — BOTTOM
#     (v0,v2,v3) → (0, −Y, …)  — FRONT  (faces toward camera at −Y)
#     (v0,v1,v2) → (−X, …)     — LEFT
#     (v0,v3,v1) → (+X, …)     — RIGHT
#
s2 = math.sqrt(2)
s6 = math.sqrt(6)

verts = [
    ( 0.0,        0.0,    1.0   ),   # v0  apex
    ( 0.0,  2*s2/3,      -1/3   ),   # v1  back base
    (-s6/3,  -s2/3,      -1/3   ),   # v2  left base
    ( s6/3,  -s2/3,      -1/3   ),   # v3  right base
]

# Each tuple: (v_indices…, material_slot, label, image_filename)
# Loop order: loop-0 maps to UV_TOP, loop-1 to UV_BL, loop-2 to UV_BR
FACE_DATA = [
    ((1, 3, 2), 0, "bottom", "bottom.png"),   # base, faces –Z
    ((0, 2, 3), 1, "front",  "front.png" ),   # faces –Y (camera side)
    ((0, 1, 2), 2, "left",   "left.png"  ),   # faces –X
    ((0, 3, 1), 3, "right",  "right.png" ),   # faces +X
]

# UV triangle: upright, fills 0-1 UV space.  loop-0=top, loop-1=BL, loop-2=BR
UV_MAP = [(0.5, 1.0), (0.0, 0.0), (1.0, 0.0)]

# ── build mesh with bmesh ──────────────────────────────────────────────────────

mesh = bpy.data.meshes.new("TetrahedronMesh")
obj  = bpy.data.objects.new("Tetrahedron", mesh)
bpy.context.collection.objects.link(obj)
bpy.context.view_layer.objects.active = obj
obj.select_set(True)

bm = bmesh.new()

bm_verts = [bm.verts.new(v) for v in verts]
bm.verts.ensure_lookup_table()

uv_layer = bm.loops.layers.uv.new("UVMap")

for face_vi, mat_idx, _label, _img in FACE_DATA:
    face = bm.faces.new([bm_verts[i] for i in face_vi])
    face.material_index = mat_idx
    for li, loop in enumerate(face.loops):
        loop[uv_layer].uv = UV_MAP[li]

bm.to_mesh(mesh)
bm.free()
mesh.update()

# ── materials ──────────────────────────────────────────────────────────────────

for _face_vi, mat_idx, label, img_file in FACE_DATA:
    mat = bpy.data.materials.new(name=label)
    mat.use_nodes = True

    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()

    out  = nodes.new("ShaderNodeOutputMaterial");  out.location  = (400,   0)
    bsdf = nodes.new("ShaderNodeBsdfPrincipled");  bsdf.location = (  0,   0)
    tex  = nodes.new("ShaderNodeTexImage");        tex.location  = (-350,   0)

    links.new(bsdf.outputs["BSDF"],    out.inputs["Surface"])
    links.new(tex.outputs["Color"],    bsdf.inputs["Base Color"])

    img_path = os.path.join(SCRIPT_DIR, img_file)
    if os.path.isfile(img_path):
        tex.image = bpy.data.images.load(img_path, check_existing=True)
        print(f"  Loaded texture: {img_path}")
    else:
        print(f"  WARNING: texture not found: {img_path}")

    obj.data.materials.append(mat)

# ── camera ─────────────────────────────────────────────────────────────────────
# Position camera so the FRONT face (facing –Y) is squarely in view.
# Camera at (0, –3.5, 1.2), tilted to look at origin.

bpy.ops.object.camera_add()
cam_obj = bpy.context.active_object
cam_obj.name = "Camera"
cam_obj.location = (0.0, -3.5, 1.2)
dx, dy, dz = 0.0 - cam_obj.location.x, 0.0 - cam_obj.location.y, 0.0 - cam_obj.location.z
cam_obj.rotation_euler = (
    math.atan2(math.sqrt(dx*dx + dy*dy), dz),
    0.0,
    math.atan2(dx, -dy),
)
bpy.context.scene.camera = cam_obj

# ── sun light ──────────────────────────────────────────────────────────────────

bpy.ops.object.light_add(type='SUN', location=(3.0, -3.0, 5.0))
sun = bpy.context.active_object
sun.name = "Sun"
sun.data.energy = 4.0
sun.rotation_euler = (math.radians(45), 0.0, math.radians(45))

# ── render settings (Cycles for preview quality) ──────────────────────────────

bpy.context.scene.render.engine = 'CYCLES'
bpy.context.scene.cycles.samples = 64
bpy.context.scene.render.resolution_x = 1280
bpy.context.scene.render.resolution_y = 720

# ── save ──────────────────────────────────────────────────────────────────────

bpy.ops.wm.save_as_mainfile(filepath=OUT_BLEND)
print(f"\nSaved: {OUT_BLEND}")
