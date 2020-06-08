uniform sampler2D bgl_RenderedTexture;

void main() {
    vec4 sum = vec4(0);
    vec2 texcoord = vec2(gl_TexCoord[0]).st;
    int j;
    int i;


    for( i= -5 ;i < 5; i++) {
        for (j = -5; j < 5; j++) {
            sum += texture2D(bgl_RenderedTexture, texcoord + vec2(j, i) * 0.0045) * 0.52;
        }
    }


    gl_FragColor = sum*sum*0.0015+texture2D(bgl_RenderedTexture, texcoord);
}


