using System.IO;
using UnityEditor;
using UnityEditor.SceneManagement;
using UnityEngine;

// The editor method the unity-batch-build pipeline runs: one scene with one cube, saved, and a JSON the judge reads.
public static class Smoke
{
    public static void Run()
    {
        var scene = EditorSceneManager.NewScene(NewSceneSetup.EmptyScene, NewSceneMode.Single);
        var cube = GameObject.CreatePrimitive(PrimitiveType.Cube);
        cube.name = "SmokeCube";
        cube.transform.position = new Vector3(1, 2, 3);
        EditorSceneManager.SaveScene(scene, "Assets/Smoke.unity");
        var json = "{\"unityVersion\":\"" + Application.unityVersion + "\",\"objects\":[\"" + cube.name + "\"]}";
        File.WriteAllText("smoke.json", json);
        AssetDatabase.SaveAssets();
    }
}
