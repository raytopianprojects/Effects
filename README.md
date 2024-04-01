A Simple Shader Compositing Library for Panda3D.

To use just download effects.py. No additional dependencies needed.

Example

```
python
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
                "fragment_attributes": "in vec2 texcoord;"},

               {"vertex": "texcoord *= 2;",
                "fragment": "p3d_FragColor.b -= 0.3;"}]
    e = Effect()
    for shader in shaders:
        e.add_layer(**shader)

    for value in range(3):
        p = s.loader.load_model("panda")
        p.set_pos((-10 * value, 0, 0))
        p.reparent_to(s.render)

        e.apply_effect(p)
    s.run()
```
