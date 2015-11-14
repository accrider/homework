import numpy as np
def main():
    obs_model = np.matrix(np.loadtxt("params/observationModel.txt", delimiter=" "))
    trans_model = np.matrix(np.loadtxt("params/transitionModel.txt", delimiter=" "))
    prior_model = np.matrix(np.loadtxt("params/priorModel.txt", delimiter=" "))
    names = [line.strip() for line in open("params/names.txt")]
    obs_train = np.matrix(np.loadtxt("observationsTrain/obsBuSF.txt", delimiter=" "))
    prior_result = [ prior_model for i in range(6) ]
    for race in range(10):
        for horse in range(5):
            predict_sf = [float(sum(np.multiply(trans_model[:,[i]], prior_result[horse].T))) for i in range(6)]
            t = np.multiply(np.matrix(predict_sf).T,obs_model[:,[int(obs_train[race,horse])]])
            prior_result[horse] = (t / sum(t)).T
    results = []
    for horse in range(5):
        predict_latent = [float(sum(np.multiply(trans_model[:,[i]], prior_result[horse].T))) for i in range(6)]
        predict_obs = [float(sum(np.multiply(obs_model[:,[i]], np.matrix(predict_latent).T))) for i in range(6)]
        exp_obs = [float(sum((idx) * i for idx, i in enumerate(predict_obs)))]
        results.append([names[horse],exp_obs,predict_latent.index(max(predict_latent))])
    for idx, i in enumerate(sorted(results, key=lambda dup : dup[1], reverse=True)):
        print(idx+1, i[0],i[1],i[2])
main()