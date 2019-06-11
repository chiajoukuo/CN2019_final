import React, { Component } from 'react';
import './App.css';
import { MediaPlayer } from 'dashjs';
import test_url from './video/MU_1/MU_1.mpd'

const player = MediaPlayer().create();
//player.initialize(document.querySelector("#videoPlayer"), "https://d206c4y6cx10lo.cloudfront.net/bk_peng_000340_22_32_10sec_spliced.mpd", true);

class App extends Component {
    state = {
        url:'/video/video/video.mpd',
        test:':)',
        videolist:['video', 'MU_1'],
        tmp:''
    }
    
    switchVideo (i) {
        player.reset();
        this.setState({
            url: '/video/'+i+'/'+i+'.mpd'
        })
        this.loadVideo('/video/'+i+'/'+i+'.mpd');
    }
    loadVideo = () => {
        player.attachView(this.video);
        player.attachSource(test_url);
    }
    switchSpeed (i) {
        document.querySelector('video').playbackRate = i        
    }
    componentDidMount() {
        console.log(this.state.test)
        // var player = MediaPlayer().create();
        //https://dash.akamaized.net/envivio/EnvivioDash3/manifest.mpd
        // player.initialize(document.querySelector("#videoPlayer"), test_url, true);
        player.initialize();
        this.loadVideo();
        // this.player.preload();
    }
    componentDidUpdate() {
        console.log(this.state.test)

        // if update is url, then create new player
        
        //player.initialize(document.querySelector("#videoPlayer"), this.state.url, true);
    }
    test () {
        this.setState({
            test: this.state.test === ':)'? ':(' :':)'
        })
    }
    PreventRedirect = (e) => {
        e.preventDefault();
        let list = {...this.state.videolist}
        console.log(list);
        list.push(this.state.tmp)
        this.setState({
            tmp:'',
            videolist:list
        })
    }
    getFileName = (e) => {
        console.log(e.target.value)
        this.setState({tmp:e.target.value})
    }
    render() {
        let OptionList = this.state.videolist.map(video=>{
            return <option value={video} onClick={()=>this.switchVideo({video})}>{video}</option>
        })
        return (
        <div>
            <h1>Hello</h1>
            <h3>Click the video name you want to watch...</h3>
            <form method="POST" enctype="multipart/form-data" action="upload.php">
                <input type="file" name="my_file" onChange={this.getFileName}/>
                <input type="submit" value="Upload" onClick={this.PreventRedirect}/>
            </form>
            <button onClick={()=>this.test()}>{this.state.test}</button>
            <form>
                <select name="travel-form">
                    {OptionList}　
                </select>
            </form>
            <div>
                <button onClick={()=>this.switchVideo('video')}>Avengers 4 Trailer</button>
                <button onClick={()=>this.switchVideo('MU_1')}>Michael Wazowski</button>
            </div>
            <video id="videoPlayer" controls width="600" ref={video => this.video=video} ></video>
            <div>
                <button onClick={()=>this.switchSpeed(0.5)}>0.5x</button>
                <button onClick={()=>this.switchSpeed(1)}>1x</button>
                <button onClick={()=>this.switchSpeed(2)}>2x</button>
            </div>            
            <script src="https://cdn.dashjs.org/latest/dash.all.min.js"></script>

        </div>
    );
  }
}

export default App;
