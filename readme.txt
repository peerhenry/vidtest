
- run with command `python main.py`
- python and vlc must have the same architecture (64 bit / 32 bit)
- norepeat means if a file is chosen it wont be repeated for at least this amount


example config

{
  "name": "build\\test",
  "sections": [
    {
      "directories": [
        {
          "path": "D:\\Files\\vids\\series",
          "exclusions": [],
          "includeSubDirs": false
        }
      ],
      "files": [
       
      ],
      "options": {
        "segmentCount": 3,
        "segmentLength": 3000,
				"noRepeat": 5
      }
    },
    {
      "directories": [
        {
          "path": "D:\\Files\\vids\\movies",
          "exclusions": [],
          "includeSubDirs": false
        }
      ],
      "options": {
        "segmentCount": 3,
        "segmentLength": 3000
      }
    }
  ]
}