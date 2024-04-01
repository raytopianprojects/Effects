from panda3d.core import Shader


class Effect:
    def __init__(self, version="#version 150"):
        self.fragment_attributes = []
        self.tess_2_attributes = []
        self.tess_1_attributes = []
        self.geometry_attributes = []
        self.version = version
        self.vertex = []
        self.fragment = []
        self.geometry = []
        self.tess_1 = []
        self.tess_2 = []
        self.uniforms = ["""// This is probably the most important uniform, transforming a model-space
// coordinate into a clip-space (ie. relative to the window) coordinate.  This
// is usually used in the vertex shader to transform p3d_Vertex and store the
// result in gl_Position.
uniform mat4 p3d_ModelViewProjectionMatrix;

// These are parts of the above matrix.
uniform mat4 p3d_ModelViewMatrix;
uniform mat4 p3d_ProjectionMatrix;
uniform mat4 p3d_ModelMatrix;
uniform mat4 p3d_ViewMatrix;
uniform mat4 p3d_ViewProjectionMatrix;

// This is the upper 3x3 of the inverse transpose of the ModelViewMatrix.  It is
// used to transform the normal vector into view-space coordinates.
uniform mat3 p3d_NormalMatrix;

// It's possible to append Inverse, Transpose, or InverseTranspose to any of the
// above matrix names to get an inverse and/or transpose version of that matrix:
uniform mat4 p3d_ProjectionMatrixInverse;
uniform mat4 p3d_ProjectionMatrixTranspose;
uniform mat4 p3d_ModelViewMatrixInverseTranspose;

// These access the Nth texture applied to the model.  The index matches up with
// the index used by p3d_MultiTexCoordN, p3d_TangentN, and p3d_BinormalN.
// The sampler type should be adjusted to match the type of the texture.
uniform sampler2D p3d_Texture0;

// As above, but "Shadow" should be appended if the texture has a shadow filter.
//uniform sampler2DShadow p3d_Texture0;

// Experimental inputs, new in 1.10.8, containing textures assigned using a
// particular TextureStage mode.  If no such texture has been assigned, a dummy
// texture is instead provided containing an appropriate default color.
uniform sampler2D p3d_TextureModulate[]; // default color: (1, 1, 1, 1)
uniform sampler2D p3d_TextureAdd[];      // default color: (0, 0, 0, 1)
uniform sampler2D p3d_TextureNormal[];   // default color: (0.5, 0.5, 1, 0)
uniform sampler2D p3d_TextureHeight[];   // default color: (0.5, 0.5, 1, 0)
uniform sampler2D p3d_TextureGloss[];    // default color: (1, 1, 1, 1)

// New in 1.10.0.  Contains the matrix generated from texture pos and scale.
uniform mat4 p3d_TextureMatrix[];

// Access the color scale applied to the node.
uniform vec4 p3d_ColorScale;

// Access the material attributes assigned via a Material object.
// Unused struct parameters may be omitted without consequence.
uniform struct p3d_MaterialParameters {
  vec4 ambient;
  vec4 diffuse;
  vec4 emission;
  vec3 specular;
  float shininess;

  // These properties are new in 1.10.
  vec4 baseColor;
  float roughness;
  float metallic;
  float refractiveIndex;
} p3d_Material;

// The sum of all active ambient light colors.
uniform struct p3d_LightModelParameters {
  vec4 ambient;
} p3d_LightModel;

// Active clip planes, in apiview space.  If there is no clip plane for a given
// index, it is guaranteed to contain vec4(0, 0, 0, 0).
uniform vec4 p3d_ClipPlane[4];

// Reports the frame time of the current frame, for animations.
uniform float osg_FrameTime;
// The time elapsed since the previous frame.
uniform float osg_DeltaFrameTime;
// New in 1.10.0. Contains the number of frames elapsed since program start.
uniform int osg_FrameNumber;

// If hardware skinning is enabled, this contains the transform of each joint.
// Superfluous array entries will contain the identity matrix.
uniform mat4 p3d_TransformTable[16];

// New in 1.10.  Contains information for each non-ambient light.
// May also be used to access a light passed as a shader input.
uniform struct p3d_LightSourceParameters {
  // Primary light color.
  vec4 color;

  // Light color broken up into components, for compatibility with legacy
  // shaders.  These are now deprecated.
  vec4 ambient;
  vec4 diffuse;
  vec4 specular;

  // View-space position.  If w=0, this is a directional light, with the xyz
  // being -direction.
  vec4 position;

  // Spotlight-only settings
  vec3 spotDirection;
  float spotExponent;
  float spotCutoff;
  float spotCosCutoff;

  // Individual attenuation constants
  float constantAttenuation;
  float linearAttenuation;
  float quadraticAttenuation;

  // constant, linear, quadratic attenuation in one vector
  vec3 attenuation;

  // Shadow map for this light source
  sampler2DShadow shadowMap;

  // Transforms view-space coordinates to shadow map coordinates
  mat4 shadowViewMatrix;
} p3d_LightSource[32];

// New in 1.10.  Contains fog state.
uniform struct p3d_FogParameters {
  vec4 color;
  float density;
  float start;
  float end;
  float scale; // 1.0 / (end - start)
} p3d_Fog;
"""]
        self.vertex_attributes = ["""// The position, normal vector and color of the currently processed vertex.
in vec4 p3d_Vertex;
in vec3 p3d_Normal;
in vec4 p3d_Color;

// The texture coordinates associated with the Nth texture.
in vec2 p3d_MultiTexCoord0;
in vec2 p3d_MultiTexCoord1;
in vec2 p3d_MultiTexCoord2;

// These are the tangent and binormal vectors, if present.  If an index is appended,
// it will use the set of binormals and tangents associated with the Nth texture.
in vec3 p3d_Binormal;
in vec3 p3d_Binormal0;
in vec3 p3d_Binormal1;
in vec3 p3d_Tangent;
in vec3 p3d_Tangent0;
in vec3 p3d_Tangent1;

// A vertex column named "anything".  The number of components should match up with
// that of the vertex array.  "uvec" and "ivec" variants are allowed for integer
// vertex arrays to access un-normalized data.
in vec4 anything;

// These two attributes will be present when hardware skinning is enabled.
// transform_index contains indices into the p3d_TransformTable array for the four
// most influential joints, and transform_weight the corresponding weights.
in vec4 transform_weight;
in uvec4 transform_index;"""]
        self.shader = None

    def add_layer(self, uniforms=None,
                  vertex_attributes=None,
                  vertex=None,
                  fragment_attributes=None,
                  fragment=None,
                  geometry_attributes=None,
                  geometry=None,
                  tess_1_attributes=None,
                  tess_1=None,
                  tess_2_attributes=None,
                  tess_2=None,
                  order=None):
        if uniforms:
            self.uniforms.append(uniforms)
        if vertex_attributes:
            self.vertex_attributes.append(vertex_attributes)
        if vertex:
            if order:
                self.vertex.insert(order, vertex)
            else:
                self.vertex.append(vertex)

        if fragment_attributes:
            self.fragment_attributes.append(fragment_attributes)
        if fragment:
            if order:
                self.fragment.insert(order, fragment)
            else:
                self.fragment.append(fragment)
        if geometry_attributes:
            self.geometry_attributes.append(geometry_attributes)
        if geometry:
            if order:
                self.geometry.insert(order, geometry)
            else:
                self.geometry.append(geometry)
        if tess_1_attributes:
            self.tess_1_attributes.append(tess_1_attributes)
        if tess_1:
            if order:
                self.tess_1.insert(order, tess_1)
            else:
                self.tess_1.append(tess_1)
        if tess_2_attributes:
            self.tess_2_attributes.append(tess_2_attributes)
        if tess_2:
            if order:
                self.tess_2.insert(order, tess_2)
            else:
                self.tess_2.append(tess_2)

        self.create_shader()

    def remove_layer(self, layers,
                     uniforms=None,
                     vertex_attributes=None,
                     vertex=None,
                     fragment_attributes=None,
                     fragment=None,
                     geometry_attributes=None,
                     geometry=None,
                     tess_1_attributes=None,
                     tess_1=None,
                     tess_2_attributes=None,
                     tess_2=None):
        for layer in layers:
            if uniforms:
                del self.uniforms[layer]
            if vertex_attributes:
                del self.vertex_attributes[layer]
            if vertex:
                del self.vertex[layer]
            if fragment_attributes:
                del self.fragment_attributes[layer]

            if fragment:
                del self.fragment[layer]
            if geometry_attributes:
                del self.geometry_attributes[layer]

            if geometry:
                del self.geometry[layer]
            if tess_1_attributes:
                del self.tess_1_attributes[layer]

            if tess_1:
                del self.tess_1[layer]
            if tess_2_attributes:
                del self.tess_2_attributes[layer]

            if tess_2:
                del self.tess_2[layer]
        self.create_shader()

    def create_shader(self):
        vertex = "\n".join(self.vertex_attributes) + "\nvoid main(){"
        tess_1 = "\nvoid main(){"
        tess_2 = "\nvoid main(){"
        geometry = "\nvoid main(){"
        fragment = "\nvoid main(){"
        uniforms = "\n".join(self.uniforms)

        if self.vertex:
            vertex += "\n".join(self.vertex)
            vertex = self.version + uniforms + vertex + "}"
        else:
            vertex = ""
        if self.fragment:
            fragment += "\n".join(self.fragment)
            fragment = self.version + uniforms + "out vec4 p3d_FragColor;" + "\n".join(
                self.fragment_attributes) + fragment + "}"
        else:
            fragment = ""
        if self.geometry:
            geometry += "\n".join(self.geometry)
            geometry = self.version + uniforms + "\n".join(self.geometry_attributes) + geometry + "}"
        else:
            geometry = ""

        if self.tess_1:
            tess_1 += "\n".join(self.tess_1)
            tess_1 = self.version + uniforms + "\n".join(self.tess_1_attributes) + tess_1 + "}"
        else:
            tess_1 = ""

        if self.tess_2:
            tess_2 += "\n".join(self.tess_2)
            tess_2 = self.version + uniforms + "\n".join(self.tess_2_attributes) + tess_2 + "}"
        else:
            tess_2 = ""
        print("vertex\n", vertex, "\nfragment\n", fragment, "\nGeometry\n", geometry, "\ntess1\n", tess_1, "\ntess2\n", tess_2)
        self.shader = Shader.make(Shader.SL_GLSL,
                                  vertex=vertex,
                                  fragment=fragment,
                                  geometry=geometry,
                                  tess_control=tess_1,
                                  tess_evaluation=tess_2)

    def apply_effect(self, nodepath):
        nodepath.set_shader(self.shader)


if __name__ == "__main__":
    from direct.showbase.ShowBase import ShowBase

    s = ShowBase()

    shaders = [{"vertex":
                    """
        gl_Position = p3d_ModelViewProjectionMatrix * p3d_Vertex;
        texcoord = p3d_MultiTexCoord0;
    """,
                "fragment": """
  vec4 color = texture(p3d_Texture0, texcoord);
  p3d_FragColor = color.bgra;
""",
                "vertex_attributes": "out vec2 texcoord;",
                "fragment_attributes": "in vec2 texcoord;"}, {"vertex": "texcoord *= 2;", "fragment": "p3d_FragColor -= 0.3;"}]
    e = Effect()
    for shader in shaders:
        e.add_layer(**shader)

    for value in range(3):
        p = s.loader.load_model("panda")
        p.set_pos((-10 * value, 0, 0))
        p.reparent_to(s.render)

        e.apply_effect(p)
    s.run()