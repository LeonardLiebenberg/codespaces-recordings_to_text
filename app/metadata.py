import pandas as pd
import os

class Metadata:
    def get_recording_dataframe(self,recordings_directory: str) -> pd.DataFrame:
        """
        Returns a pandas dataframe containing the list of audio file names in a directory and their corresponding call IDs
        """
        file_names = [f for f in os.listdir(recordings_directory) if os.path.isfile(os.path.join(recordings_directory, f))]
        frame = pd.DataFrame(file_names, columns=['AudioFileName'])
        id_reg = r'_(\d+)_'
        frame['call_id'] = frame['AudioFileName'].str.extract(id_reg, expand=False)
        frame['call_id'] = frame['call_id'].astype('int')
        return frame

    def get_call_dataframe(self,pgengine: object,recordings_directory: str) -> pd.DataFrame:
        """
        Returns a pandas dataframe containing the call details for the given call IDs
        """
        rls = self.get_recording_dataframe(recordings_directory).call_id.tolist()
        calls_query = "SELECT c.call_id,u.username,c.number,c.call_date,c.disposition_name FROM calls c LEFT JOIN users u on u.id = CAST(c.username AS BIGINT) WHERE c.call_id = ANY(%(_rls)s) AND c.username SIMILAR TO '[0-9]%%'"
        queryParams = {'_rls': rls}
        with pgengine.connect() as con:
            cdf = pd.read_sql(sql=calls_query, con=con, params=queryParams)
        cdf.call_id = cdf.call_id.astype('int')
        return cdf
    
    def create_metadata_file(self, recording_df: pd.DataFrame, call_df: pd.DataFrame) -> pd.DataFrame:
        """
        Returns a pandas dataframe containing metadata for the recordings by merging recordings dataframe and calls dataframe
        """
        metadata = pd.merge(call_df,recording_df, on='call_id', how='left')
        metadata.rename(columns={'username': 'AgentName', 'number': 'CustomerPhoneNumber', 'call_date': 'Timestamp', 'disposition_name': 'CallType'}, inplace=True)
        metadata['CallCentre'] = 'PassiveHouse'
        metadata['Team'] = 'Collections'
        metadata['AgentName'] = metadata['AgentName'].fillna('Unknown')
        metadata['Timestamp'] = pd.to_datetime(metadata['Timestamp']).dt.strftime('%Y-%m-%d %H:%M:%S')
        metadata.drop(['call_id'], axis=1, inplace=True)
        return metadata